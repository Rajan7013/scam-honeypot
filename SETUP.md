# 🚀 QUICK START GUIDE

## ⚡ 3-Minute Setup

### Step 1: Get Gemini API Key (1 minute)
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key" (sign in with Google if needed)
3. Copy the API key (starts with `AIzaSy...`)

### Step 2: Configure Project (1 minute)
1. Open the `.env` file in the project root
2. Find the line: `GEMINI_API_KEY=PASTE_YOUR_API_KEY_HERE`
3. Replace `PASTE_YOUR_API_KEY_HERE` with your actual API key
4. Save the file

### Step 3: Install & Run (1 minute)
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python start.py
```

### Step 4: Open Dashboard
Go to: http://localhost:8000/static/dashboard.html

---

## 🎯 What to Test

### Test 1: Scam Detection
**Try this message:**
```
Congratulations! You won 10 lakh rupees in lucky draw. 
Click this link to claim: bit.ly/claim123
```

**Expected Result:**
- 🚨 SCAM DETECTED
- Confidence: 85-95%
- Type: lottery_scam

### Test 2: AI Engagement
**Select Persona:** Ramesh (Elderly)

**Try this message:**
```
Hello sir, your bank account will be blocked. 
Please verify by sharing OTP.
```

**Expected Result:**
- AI responds as confused elderly person
- Asks clarifying questions
- Shows concern about account

### Test 3: Intelligence Extraction
**Try this message:**
```
Transfer money to 9876543210@paytm or call 9999999999
```

**Expected Result:**
- Extracts UPI ID: 9876543210@paytm
- Extracts Phone: 9999999999
- Shows confidence scores

---

## 🎭 Demo Scenarios

### Scenario 1: UPI Fraud (5 messages)
1. "Hello sir, I am from Paytm customer care."
2. "Your account has some issue. Share your mobile number."
3. "Now share the OTP we sent."
4. "Also share your UPI PIN for verification."
5. "Transfer 100 to 9876543210@paytm to activate."

**Watch:** AI stays in character, gradually extracts information

### Scenario 2: Bank Phishing (3 messages)
1. "Your account will be blocked in 24 hours."
2. "Click this link: bit.ly/kyc-update"
3. "Or call 1800-123-4567 immediately."

**Watch:** High scam confidence, URL extraction

### Scenario 3: Investment Scam (4 messages)
1. "Amazing investment opportunity!"
2. "Invest 10,000, get 1 lakh in 30 days."
3. "Transfer to account: 123456789012"
4. "Or UPI: investor@paytm"

**Watch:** Multiple intelligence extractions

---

## 🐛 Troubleshooting

### Error: "GEMINI_API_KEY not configured"
**Solution:**
1. Make sure you created `.env` file (not `.env.example`)
2. Open `.env` and add your actual API key
3. Restart the server

### Error: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
```

### Port 8000 already in use
**Solution:**
```bash
# Use different port
python -m uvicorn app.main:app --port 8001
```

### API not responding
**Solution:**
1. Check if server is running (should see "Uvicorn running")
2. Check console for errors
3. Make sure Gemini API key is valid

---

## 📊 Dashboard Features

### Stats Dashboard
- **Total Scans**: Number of messages analyzed
- **Scams Detected**: Number of scams found
- **Active Chats**: Ongoing conversations
- **Intel Extracted**: Total intelligence items

### Scam Detection Test
- Enter any message
- Get instant scam analysis
- See confidence score and type
- View detailed explanation

### AI Engagement Test
- Choose persona (or random)
- Enter scammer message
- Get AI response
- See extracted intelligence

### Conversation History
- View all active conversations
- See message counts
- Track intelligence extracted
- Auto-refreshes every 10 seconds

---

## ⌨️ Keyboard Shortcuts

- **Ctrl + Enter** in text area: Submit/Analyze
- Works in both detection and engagement sections

---

## 🎬 Ready to Demo!

Your system is now ready for the hackathon demo. Here's what makes it special:

✅ **Fully functional** - All features working end-to-end
✅ **Zero cost** - 100% free tools and APIs
✅ **Beautiful UI** - Premium design with stats dashboard
✅ **Smart AI** - 3 believable personas
✅ **Real extraction** - 8 types of intelligence data
✅ **Live demo ready** - Can show actual scammer engagement

**Next:** Practice your demo with the scenarios above!
