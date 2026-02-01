# 🚀 GROQ API SETUP - 2 MINUTES!

## Why Groq is Better:

✅ **FREE** - Generous free tier
✅ **FAST** - 10x faster than Gemini (uses LPU chips)
✅ **HIGH LIMITS** - 30 requests/minute (vs Gemini's quota issues)
✅ **NO QUOTA ERRORS** - Much more reliable

---

## Step 1: Get Groq API Key (1 minute)

1. Go to: **https://console.groq.com/keys**
2. Sign up with Google/GitHub (FREE)
3. Click "Create API Key"
4. Give it a name (e.g., "Scam Honeypot")
5. Copy the key (starts with `gsk_...`)

---

## Step 2: Add to .env File (30 seconds)

1. Open `.env` file in project root
2. Find this line:
   ```
   GROQ_API_KEY=PASTE_YOUR_GROQ_KEY_HERE
   ```
3. Replace with your actual key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
4. Make sure this line says:
   ```
   AI_PROVIDER=groq
   ```
5. Save the file

---

## Step 3: Install Groq Package (30 seconds)

```bash
pip install groq
```

---

## Step 4: Restart Server

```bash
# Stop current server (Ctrl+C)
python start.py
```

---

## ✅ Verification

You should see:
```
✅ Groq API initialized successfully
```

NOT:
```
⚠️ Warning: Could not initialize Groq API
```

---

## 🎯 Test It!

1. Open: http://localhost:8000/static/dashboard.html
2. Select persona: Ramesh
3. Enter: "Your account blocked. Share OTP."
4. Click "Start Engagement"
5. Should get **INSTANT** AI response (not fallback!)

---

## 🆚 Groq vs Gemini Comparison

| Feature | Groq | Gemini |
|---------|------|--------|
| **Speed** | ⚡ 10x faster | Slower |
| **Free Tier** | 30 req/min | 15 req/min |
| **Quota Issues** | ✅ Rare | ❌ Common |
| **Model** | Llama 3.3 70B | Gemini 2.5 |
| **Quality** | Excellent | Excellent |
| **Cost** | FREE | FREE |

**Winner: Groq** 🏆

---

## 🔄 Switch Between Providers

Want to use Gemini instead? Just change in `.env`:

```bash
# Use Groq (Recommended)
AI_PROVIDER=groq

# OR use Gemini
AI_PROVIDER=gemini
```

---

## 🐛 Troubleshooting

### Error: "GROQ_API_KEY not configured"
**Solution**: Make sure you added the key to `.env` file and restarted server

### Error: "Module 'groq' not found"
**Solution**: Run `pip install groq`

### Still using fallback responses
**Solution**: 
1. Check `.env` has correct API key
2. Check `AI_PROVIDER=groq` in `.env`
3. Restart server

---

## ✨ YOU'RE DONE!

Your AI will now use Groq - **MUCH FASTER** and **NO QUOTA ISSUES**! 🚀

**Total setup time: 2 minutes**
