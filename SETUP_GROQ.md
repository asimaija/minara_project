# Zenvirox AI — Groq Chatbot Setup

## Quick Start

### 1. Set your Groq API Key
Get your free key at: https://console.groq.com

**Option A — Environment variable (RECOMMENDED / secure):**
```bash
export GROQ_API_KEY="gsk_your_key_here"
python manage.py runserver
```
On hosting (Railway, Render, Heroku, VPS):
- Add `GROQ_API_KEY` as an environment variable in your dashboard

**Option B — Direct browser mode (quick test only):**
In `home.html`, find this near line 1038:
```js
const GROQ_USE_DIRECT = false;
const GROQ_DIRECT_KEY = 'gsk_PASTE_YOUR_GROQ_KEY_HERE';
```
Change `GROQ_USE_DIRECT = true` and paste your key into `GROQ_DIRECT_KEY`.
⚠️ WARNING: Key will be visible in browser source. Use only for local testing!

### 2. Run migrations & start
```bash
pip install django
python manage.py migrate
python manage.py runserver
```

### 3. WhatsApp
WhatsApp is set to: +92 332 5384557
Click "Chat on WhatsApp" in the chatbot panel to open WhatsApp directly.

## Chatbot Features
- Powered by Groq (llama-3.3-70b-versatile) — ultra-fast responses
- Rich knowledge base: services, projects, pricing, process, tech stack
- WhatsApp CTA button built-in
- Secure server-side API key via Django /chat/ endpoint
- Fallback to direct mode for quick testing

## Model
Default: `llama-3.3-70b-versatile`
To change, update `GROQ_MODEL` in `home.html` or `views.py`
Other fast options: `llama-3.1-8b-instant`, `mixtral-8x7b-32768`
