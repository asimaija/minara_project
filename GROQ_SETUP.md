# 🤖 Chatbot Setup Guide — Dodos Code

## Option 1: FREE Groq API (RECOMMENDED — Llama 3.3 70B)
1. Go to: https://console.groq.com
2. Sign up free (no credit card needed)
3. Click "API Keys" → "Create API Key"
4. Copy your key (starts with `gsk_`)
5. Open your `.env` file and paste:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
6. Restart server: `python manage.py runserver`
7. Test: type "hello" in the chat widget ✅

## Option 2: No API Key (Keyword Fallback)
The chatbot ALREADY WORKS without any API key!
It uses keyword matching from `core/chatbot_dataset.json`.
Responses are slightly simpler but still answer all common questions.

## How the Chatbot is Trained:
- **Knowledge base** is in `core/views.py` → `DODOS_DATASET` variable
- **Keyword responses** are in `core/chatbot_dataset.json`
- To add new Q&A: edit the JSON file and add to `DODOS_DATASET`

## Updating the Dataset:
Edit `core/chatbot_dataset.json`:
```json
{
  "pattern": ["your keywords", "trigger words"],
  "response": "Your reply text here"
}
```

## Testing Chat API:
```bash
curl -X POST http://127.0.0.1:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "hello"}]}'
```
