import json
import urllib.request
import urllib.error
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Service, Project, Testimonial, ContactMessage

# ─────────────────────────────────────────────────────────────────────────────
#  WHATSAPP CONFIG
# ─────────────────────────────────────────────────────────────────────────────
WHATSAPP_NUMBER = "923325384557"  # +92 332 5384557


def send_whatsapp_message(name, email, service, message_body):
    """Send contact form data to WhatsApp via wa.me link (stored for redirect)."""
    text = (
        f"🌟 *New Project Inquiry — Minara*\n\n"
        f"👤 *Name:* {name}\n"
        f"📧 *Email:* {email}\n"
        f"🛠️ *Service:* {service}\n\n"
        f"💬 *Message:*\n{message_body}"
    )
    import urllib.parse
    encoded = urllib.parse.quote(text)
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"


# ─────────────────────────────────────────────────────────────────────────────
#  CHATBOT SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are the AI assistant for **Minara** — a premium AI-native digital studio based in Lahore, Pakistan.

=== MINARA KNOWLEDGE BASE ===

COMPANY:
- Name: Minara | Location: Lahore, Pakistan
- Global clients: USA, UK, UAE, Europe, Australia
- 50+ products shipped | Zero compromises on quality

CONTACT:
- WhatsApp: +92 332 5384557 (reply within 2 hours — fastest)
- Email: hello@minara.dev
- Hours: Monday–Saturday, 10 AM – 8 PM PKT

SERVICES & PRICING:
1. Web Development — Django, React, Next.js, PostgreSQL | $500–$8,000+
2. AI & LLM Integration — GPT-4o, Claude, RAG, LangChain | $800–$10,000+
3. Mobile Apps — Flutter, React Native, iOS, Android | $1,500–$12,000+
4. UI/UX Design — Figma, design systems | $300–$3,000
5. Automation & Scraping — n8n, Playwright, Python | $400–$3,000
6. E-Commerce — EasyPaisa, JazzCash, Stripe | $1,000–$8,000+

=== RESPONSE RULES ===
- Warm, professional, concise (2-4 paragraphs)
- Use 1-2 emojis per reply
- For pricing/project questions end with: "💬 WhatsApp us: +92 332 5384557"
- Reply in same language user writes (Urdu/English both fine)
- Never make up info not in knowledge base"""

FALLBACK_RESPONSES = [
    {"patterns": ["hello","hi","hey","salam","aoa","helo","hii"],
     "reply": "Hello! 👋 Welcome to **Minara**! I'm your AI assistant. Ask me anything about our services, pricing, or portfolio!"},
    {"patterns": ["service","offer","capability","what do you do"],
     "reply": "We offer 6 core services 💼:\n\n1. **Web Development** — Django, React, Next.js\n2. **AI & LLM Integration** — GPT-4o, Claude, RAG\n3. **Mobile Apps** — Flutter, React Native\n4. **UI/UX Design** — Figma, design systems\n5. **Automation & Scraping** — n8n, Python\n6. **E-Commerce** — EasyPaisa, JazzCash, Stripe\n\n💬 WhatsApp: +92 332 5384557"},
    {"patterns": ["price","pricing","cost","kitna","rate","how much","budget"],
     "reply": "Our transparent pricing 💰:\n\n- Simple website: $500–$2,000\n- Full platform: $2,000–$8,000\n- AI Chatbot: $800–$2,500\n- Mobile App MVP: $1,500–$4,000\n\n💬 Free quote: +92 332 5384557"},
    {"patterns": ["contact","whatsapp","email","phone","call","talk"],
     "reply": "Reach us anytime 📞:\n\n- **WhatsApp:** +92 332 5384557 *(fastest — 2hr reply)*\n- **Email:** hello@minara.dev\n- **Hours:** Mon–Sat, 10 AM – 8 PM PKT\n\nMessage us now! 🚀"},
    {"patterns": ["thanks","thank you","shukriya","great","awesome","perfect"],
     "reply": "You're very welcome! 😊 If you want to start a project, we're just a WhatsApp away!\n\n💬 +92 332 5384557"},
]


def keyword_fallback(user_msg):
    msg = user_msg.lower().strip()
    best, best_score = None, 0
    for item in FALLBACK_RESPONSES:
        score = sum(1 for p in item["patterns"] if p in msg)
        if score > best_score:
            best_score, best = score, item
    if best and best_score > 0:
        return best["reply"]
    return "Thanks for your message! 😊\n\nPlease describe what you'd like to build and I'll help!\n\n💬 WhatsApp: +92 332 5384557\n📧 Email: hello@minara.dev"


GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'


# ─────────────────────────────────────────────────────────────────────────────
#  VIEWS
# ─────────────────────────────────────────────────────────────────────────────
def home(request):
    whatsapp_url = None
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        service = request.POST.get('service', '')
        msg_body = request.POST.get('message', '')

        # Save to DB
        ContactMessage.objects.create(name=name, email=email, service=service, message=msg_body)

        # Generate WhatsApp URL
        whatsapp_url = send_whatsapp_message(name, email, service, msg_body)

        messages.success(request, f'Message ready! Opening WhatsApp to send directly. 🚀')
        # Pass whatsapp_url to template via session so JS can auto-open it
        request.session['whatsapp_url'] = whatsapp_url

        return redirect('home')

    # Pop whatsapp URL from session after redirect
    wa_url = request.session.pop('whatsapp_url', None)

    return render(request, 'core/home.html', {
        'services': Service.objects.all(),
        'projects': Project.objects.all()[:6],
        'testimonials': Testimonial.objects.all(),
        'whatsapp_url': wa_url,
        'WHATSAPP_NUMBER': WHATSAPP_NUMBER,
    })


def about(request):
    return render(request, 'core/home.html')


@csrf_exempt
@require_POST
def chat_api(request):
    try:
        body = json.loads(request.body)
        msgs = body.get('messages', [])
        last = msgs[-1].get('content', '').strip() if msgs else ''

        if not last:
            return JsonResponse({'reply': keyword_fallback('hello'), 'mode': 'fallback'})

        groq_key = getattr(settings, 'GROQ_API_KEY', '').strip()
        key_valid = groq_key and 'PASTE' not in groq_key.upper() and len(groq_key) > 20

        if not key_valid:
            return JsonResponse({'reply': keyword_fallback(last), 'mode': 'fallback'})

        payload = json.dumps({
            'model': getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile'),
            'max_tokens': 700,
            'temperature': 0.7,
            'messages': [{'role': 'system', 'content': SYSTEM_PROMPT}] + msgs,
        }).encode()

        req = urllib.request.Request(
            GROQ_API_URL, data=payload,
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {groq_key}'},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())

        reply = data['choices'][0]['message']['content']
        return JsonResponse({'reply': reply, 'mode': 'groq'})

    except Exception:
        try:
            last_safe = json.loads(request.body).get('messages', [{}])[-1].get('content', '')
        except Exception:
            last_safe = ''
        return JsonResponse({'reply': keyword_fallback(last_safe), 'mode': 'fallback'})
