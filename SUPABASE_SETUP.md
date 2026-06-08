# Minara + Supabase Setup Guide

## 1. Rename Project: Dodos Code → Minara

### Step 1: Rename the inner config folder
```bash
mv dodos_code minara_config
```

### Step 2: Update manage.py
```python
# manage.py — change this line:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minara_config.settings')
```

### Step 3: Update wsgi.py and asgi.py inside minara_config/
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minara_config.settings')
```

### Step 4: Update settings.py ROOT_URLCONF and WSGI_APPLICATION
```python
ROOT_URLCONF = 'minara_config.urls'
WSGI_APPLICATION = 'minara_config.wsgi.application'
```

---

## 2. Supabase Setup (Replace SQLite with Supabase PostgreSQL)

### Step 1: Create a Supabase Project
1. Go to https://supabase.com
2. Click "New Project"
3. Name it: **minara**
4. Choose region: **Southeast Asia (Singapore)** — closest to Pakistan
5. Set a strong database password and save it
6. Wait ~2 minutes for project to provision

### Step 2: Get Your Supabase Database URL
1. In Supabase dashboard → **Settings** → **Database**
2. Copy the **Connection String** (URI format):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```

### Step 3: Install psycopg2
```bash
pip install psycopg2-binary dj-database-url python-dotenv
```

### Step 4: Update your .env file
```env
# .env
SECRET_KEY=your-secret-key-here
DEBUG=True

# Supabase PostgreSQL
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

# Or use individual settings:
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-supabase-password
DB_HOST=db.[PROJECT-REF].supabase.co
DB_PORT=5432

# Groq AI (optional)
GROQ_API_KEY=your-groq-key-here

# WhatsApp (already hardcoded: +92 332 5384557)
WHATSAPP_NUMBER=923325384557
```

### Step 5: Update settings.py
```python
import dj_database_url
import os
from dotenv import load_dotenv

load_dotenv()

# ── SUPABASE DATABASE ──────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Fallback to individual settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'postgres'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
```

### Step 6: Run Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata core/fixtures/initial_projects.json
```

### Step 7: Verify Connection
```bash
python manage.py dbshell
# Should connect to Supabase PostgreSQL
```

---

## 3. Supabase Storage (For File Uploads / Images)

### Install boto3
```bash
pip install django-storages boto3
```

### In Supabase Dashboard:
1. Go to **Storage** → **New Bucket** → name it `minara-media`
2. Make it **Public**
3. Go to **Settings** → **API** → copy your **anon/public key** and **URL**

### settings.py for Supabase Storage
```python
# Add to INSTALLED_APPS:
INSTALLED_APPS += ['storages']

# Supabase Storage via S3-compatible API
AWS_ACCESS_KEY_ID = os.environ.get('SUPABASE_STORAGE_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('SUPABASE_STORAGE_SECRET')
AWS_STORAGE_BUCKET_NAME = 'minara-media'
AWS_S3_ENDPOINT_URL = 'https://[PROJECT-REF].supabase.co/storage/v1/s3'
AWS_S3_CUSTOM_DOMAIN = f'[PROJECT-REF].supabase.co/storage/v1/object/public/minara-media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
```

---

## 4. Supabase Realtime (Optional: Live Contact Notifications)

You can use Supabase Realtime to get instant notifications when someone submits the contact form.

### In your views.py, after saving ContactMessage:
```python
import httpx

def notify_supabase_realtime(message_data):
    """Broadcast new contact to Supabase Realtime channel."""
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_ANON_KEY')
    
    # Insert directly to Supabase REST API (triggers Realtime)
    response = httpx.post(
        f"{supabase_url}/rest/v1/contact_messages",
        headers={
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json",
        },
        json=message_data
    )
    return response.status_code == 201
```

---

## 5. WhatsApp Form Integration (Already Implemented!)

The contact form in Minara is already configured to:

1. **Save** the message to your database (SQLite → Supabase after setup)
2. **Auto-open WhatsApp** with the message pre-filled to **+92 332 5384557**

### How it works:
```python
# views.py — send_whatsapp_message()
WHATSAPP_NUMBER = "923325384557"

def send_whatsapp_message(name, email, service, message_body):
    text = f"🌟 *New Project Inquiry — Minara*\n\n👤 *Name:* {name}\n📧 *Email:* {email}\n🛠️ *Service:* {service}\n\n💬 *Message:*\n{message_body}"
    encoded = urllib.parse.quote(text)
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"
```

When the form is submitted:
- Message saves to DB ✅
- Page redirects back ✅  
- WhatsApp opens automatically with the pre-filled message ✅
- User clicks "Send" in WhatsApp to deliver the message ✅

---

## 6. Full Deployment (Production)

### Install requirements
```bash
pip install gunicorn whitenoise
```

### settings.py production additions
```python
ALLOWED_HOSTS = ['minara.dev', 'www.minara.dev', 'your-server-ip']
DEBUG = False
STATIC_ROOT = BASE_DIR / 'staticfiles'
MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Collect static files
```bash
python manage.py collectstatic
```

### Run with Gunicorn
```bash
gunicorn minara_config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

---

## 7. Quick Start Commands

```bash
# Clone / enter project
cd minara_project

# Install dependencies
pip install -r requirements.txt
pip install psycopg2-binary dj-database-url python-dotenv

# Setup .env (copy .env.example and fill in Supabase URL)
cp .env.example .env
# Edit .env with your Supabase DATABASE_URL

# Run migrations (creates tables in Supabase)
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load sample data
python manage.py loaddata core/fixtures/initial_projects.json

# Start server
python manage.py runserver
```

**Your Minara site will be live at:** http://127.0.0.1:8000

---

## Summary of Changes: Dodos Code → Minara

| What changed | Old value | New value |
|---|---|---|
| Site name | Dodos Code | Minara |
| Brand color | Maroon/Gold (#6b0f2b) | Azure/Cyan (#0a2fff / #00d4ff) |
| Font | Playfair Display / Outfit | Syne / DM Sans |
| 3D scene | Generic nodes | DNA helix + neural brain + torus rings |
| Contact form | Email only | **WhatsApp +92 332 5384557** auto-opens |
| Database | SQLite | Supabase PostgreSQL (see above) |
| Email | hello@dodoscode.com | hello@minara.dev |
