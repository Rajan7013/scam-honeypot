# 🚀 DEPLOYMENT GUIDE - Render.com

## 📋 Prerequisites

- GitHub account
- Render.com account (free tier)
- Your code pushed to GitHub

---

## 🔧 Step 1: Prepare for Deployment

### **1.1 Create `requirements.txt`**
Already done! ✅

### **1.2 Create `render.yaml`** (Optional but recommended)

Create file: `render.yaml`

```yaml
services:
  - type: web
    name: agentic-honeypot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python start.py
    envVars:
      - key: GROQ_API_KEY
        sync: false
      - key: HACKATHON_API_KEY
        sync: false
      - key: AI_PROVIDER
        value: groq
      - key: PORT
        value: 8000
```

### **1.3 Update `start.py` for Production**

Already configured! ✅ (Uses environment variables)

---

## 🌐 Step 2: Deploy to Render

### **2.1 Push to GitHub**

```bash
git init
git add .
git commit -m "Initial commit - Agentic Honey-Pot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/scam-honeypot.git
git push -u origin main
```

### **2.2 Create Render Account**

1. Go to: https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### **2.3 Create New Web Service**

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select `scam-honeypot` repo

### **2.4 Configure Service**

**Settings:**
- **Name:** `agentic-honeypot` (or your choice)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python start.py`
- **Instance Type:** `Free`

### **2.5 Add Environment Variables**

Click **"Environment"** tab and add:

| Key | Value |
|-----|-------|
| `GROQ_API_KEY` | `your-actual-groq-key` |
| `HACKATHON_API_KEY` | `your-secret-api-key-123` |
| `AI_PROVIDER` | `groq` |
| `PORT` | `8000` |
| `HOST` | `0.0.0.0` |

### **2.6 Deploy!**

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. You'll get a URL like: `https://agentic-honeypot.onrender.com`

---

## ✅ Step 3: Test Your Deployment

### **3.1 Test Health Endpoint**

```bash
curl https://your-app.onrender.com/health
```

**Expected:**
```json
{"status": "healthy", "service": "Agentic Honey-Pot"}
```

### **3.2 Test Webhook Endpoint**

```bash
curl -X POST https://your-app.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-123" \
  -d '{
    "message": "Your account will be blocked. Share OTP now!"
  }'
```

**Expected:**
```json
{
  "scam_detected": true,
  "confidence": 0.95,
  "agent_engaged": true,
  "conversation_turns": 1,
  "extracted_intelligence": {...},
  "agent_response": "What is OTP? I'm confused...",
  "conversation_id": "...",
  "agent_persona": "Ramesh Kumar",
  "scam_type": "phishing"
}
```

### **3.3 Test Dashboard**

Visit: `https://your-app.onrender.com/static/dashboard.html`

---

## 🔒 Step 4: Security

### **4.1 API Key**

Your `HACKATHON_API_KEY` is required for webhook access:
- Set it in Render environment variables
- Share it with hackathon organizers
- Don't commit it to GitHub!

### **4.2 HTTPS**

Render provides free HTTPS automatically! ✅

---

## 📊 Step 5: Monitor Deployment

### **5.1 View Logs**

In Render dashboard:
1. Go to your service
2. Click **"Logs"** tab
3. Watch for:
   ```
   ✅ Groq API initialized successfully
   🤖 Autonomous Agent started
   ```

### **5.2 Check Status**

- **Dashboard:** Shows service status (Running/Failed)
- **Metrics:** CPU, Memory usage
- **Events:** Deployment history

---

## 🎯 Step 6: Submit to Hackathon

### **6.1 Your Submission Details**

**Public API Endpoint:**
```
https://your-app.onrender.com/webhook
```

**API Key:**
```
your-secret-api-key-123
```

**Documentation:**
```
https://your-app.onrender.com/docs
```

**Dashboard:**
```
https://your-app.onrender.com/static/dashboard.html
```

### **6.2 Test with Mock Scammer API**

Once deployed, the hackathon's Mock Scammer API will send messages to your webhook.

---

## 🐛 Troubleshooting

### **Issue: Build Failed**

**Solution:** Check `requirements.txt` has all dependencies

### **Issue: Service Crashes**

**Solution:** Check logs for errors, ensure environment variables are set

### **Issue: 401 Unauthorized**

**Solution:** Verify `X-API-Key` header matches `HACKATHON_API_KEY`

### **Issue: Slow Response**

**Solution:** Render free tier may sleep after inactivity (30 min warmup)

---

## 🚀 Alternative: Railway.app

If Render doesn't work, try Railway:

1. Go to: https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub"**
4. Select your repo
5. Add environment variables
6. Deploy!

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created
- [ ] Environment variables added
- [ ] Service deployed successfully
- [ ] Health endpoint tested
- [ ] Webhook endpoint tested
- [ ] API key working
- [ ] Dashboard accessible
- [ ] Logs showing no errors
- [ ] Public URL shared with hackathon

---

## 🎉 You're Live!

Your agentic honey-pot is now running 24/7 in the cloud, ready to catch scammers!

**Public URL:** `https://your-app.onrender.com`
