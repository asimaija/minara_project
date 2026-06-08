# ═══════════════════════════════════════════════════════════
# SUPABASE FULL SETUP GUIDE — MINARA
# ═══════════════════════════════════════════════════════════

## STEP 1 — Create a Supabase Project

1. Go to https://supabase.com → Click "Start your project"
2. Sign in with GitHub
3. Click "New Project"
4. Fill in:
   - Organization: (your org or personal)
   - Name: minara-prod
   - Database Password: (save this securely!)
   - Region: Southeast Asia (Singapore) — closest to Lahore
5. Click "Create new project" — wait ~2 minutes

---

## STEP 2 — Create the Contact Messages Table

In Supabase dashboard → go to **SQL Editor** → Run this SQL:

```sql
-- Contact messages table
CREATE TABLE contact_messages (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  service TEXT,
  message TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  is_read BOOLEAN DEFAULT FALSE,
  replied_at TIMESTAMPTZ
);

-- Enable Row Level Security
ALTER TABLE contact_messages ENABLE ROW LEVEL SECURITY;

-- Allow inserts from anon (for the contact form)
CREATE POLICY "Allow public inserts" ON contact_messages
  FOR INSERT TO anon
  WITH CHECK (true);

-- Only authenticated users can read/update
CREATE POLICY "Auth users can read all" ON contact_messages
  FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "Auth users can update" ON contact_messages
  FOR UPDATE TO authenticated
  USING (true);
```

---

## STEP 3 — Get Your API Keys

In Supabase dashboard → **Project Settings** → **API**

Copy these two values:
- **Project URL** → looks like: `https://abcdefghijk.supabase.co`
- **anon/public key** → long JWT string starting with `eyJ...`

---

## STEP 4 — Add to Django settings.py

Open `dodos_code/settings.py` and add:

```python
# Supabase Configuration
SUPABASE_URL = 'https://YOUR_PROJECT_ID.supabase.co'
SUPABASE_ANON_KEY = 'eyJ...'  # your anon/public key
SUPABASE_SERVICE_KEY = 'eyJ...'  # your service_role key (for admin ops)
```

Or better, use environment variables:

```python
import os

SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', '')
```

Then create a `.env` file in the project root:
```
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...
```

Install python-dotenv:
```bash
pip install python-dotenv
```

Add to top of settings.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## STEP 5 — Install Supabase Python Client

```bash
pip install supabase
```

Add to `requirements.txt`:
```
supabase>=2.0.0
```

---

## STEP 6 — Update views.py

Replace the `home` view in `core/views.py`:

```python
from django.conf import settings

# Add this helper function
def save_to_supabase(name, email, service, message_body):
    """Save contact form data to Supabase."""
    try:
        from supabase import create_client
        supabase_url = getattr(settings, 'SUPABASE_URL', '')
        supabase_key = getattr(settings, 'SUPABASE_ANON_KEY', '')
        
        if not supabase_url or not supabase_key:
            return False
        
        client = create_client(supabase_url, supabase_key)
        client.table('contact_messages').insert({
            'name': name,
            'email': email,
            'service': service,
            'message': message_body,
        }).execute()
        return True
    except Exception as e:
        print(f'Supabase error: {e}')
        return False


def home(request):
    # Handle AJAX form submission (no popup, no redirect)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        service = request.POST.get('service', '')
        msg_body = request.POST.get('message', '')

        # Save to Django DB
        ContactMessage.objects.create(
            name=name, email=email,
            service=service, message=msg_body
        )

        # Also save to Supabase
        save_to_supabase(name, email, service, msg_body)

        # If AJAX request, return JSON (no redirect)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.http import JsonResponse
            return JsonResponse({'status': 'ok', 'message': 'Message received!'})

        # Fallback for non-JS: redirect back
        messages.success(request, 'Message sent successfully!')
        return redirect('home')

    return render(request, 'core/home.html', {
        'services': Service.objects.all(),
        'projects': Project.objects.all()[:6],
        'testimonials': Testimonial.objects.all(),
        'SUPABASE_URL': getattr(settings, 'SUPABASE_URL', ''),
        'SUPABASE_ANON_KEY': getattr(settings, 'SUPABASE_ANON_KEY', ''),
        'WHATSAPP_NUMBER': WHATSAPP_NUMBER,
    })
```

---

## STEP 7 — Pass Supabase Keys to Frontend

Add this in home.html `<head>` (before closing `</head>`):

```html
<!-- Supabase config for frontend (anon key is safe to expose) -->
<script>
  window.SUPABASE_URL = "{{ SUPABASE_URL }}";
  window.SUPABASE_KEY = "{{ SUPABASE_ANON_KEY }}";
</script>
```

The contact form in home.html already uses `window.SUPABASE_URL` and
`window.SUPABASE_KEY` to save to Supabase directly. The form sends via
AJAX — no popup, no redirect, just an inline success message.

---

## STEP 8 — View Messages in Supabase Dashboard

1. Go to **Table Editor** in Supabase
2. Click `contact_messages`
3. You'll see all submissions in real-time!

You can also enable **Email Notifications** using Supabase Edge Functions
or set up a **Webhook** to ping your Slack/WhatsApp when a new message arrives.

---

## STEP 9 — (Optional) Realtime Notifications

To get WhatsApp notifications when a form is filled, add this to
Supabase → **Database** → **Webhooks**:

1. Create a webhook on `contact_messages` table INSERT
2. Point it to a Zapier/Make webhook
3. Configure Zapier to send WhatsApp via Twilio or wa.me

---

## QUICK CHECKLIST

- [ ] Supabase project created
- [ ] `contact_messages` table created with SQL above
- [ ] API keys copied to settings.py / .env
- [ ] `pip install supabase` done
- [ ] `save_to_supabase()` function added to views.py
- [ ] `SUPABASE_URL` and `SUPABASE_ANON_KEY` passed to template context
- [ ] `<script>window.SUPABASE_URL...</script>` added to home.html head
- [ ] Test by submitting the contact form
- [ ] Check Supabase Table Editor to confirm data saved

