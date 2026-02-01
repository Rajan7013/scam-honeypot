# 🕵️ Agentic Honey-Pot: AI-Powered Scam Detection System

An autonomous AI system that detects scam messages and engages scammers using believable personas to extract intelligence (bank accounts, UPI IDs, phishing links).

## 🎯 Features

- **Scam Detection**: AI-powered detection of various scam types (UPI fraud, phishing, lottery scams)
- **Autonomous Engagement**: Believable AI personas that engage scammers naturally
- **Intelligence Extraction**: Automatically extracts bank accounts, UPI IDs, phone numbers, and URLs
- **Real-time Dashboard**: Monitor conversations and extracted intelligence
- **RESTful API**: Easy integration with JSON request/response format

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google Gemini API key ([Get it FREE here](https://makersuite.google.com/app/apikey))

### Installation

```bash
# 1. Navigate to project
cd scam-honeypot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
# Open .env file and replace PASTE_YOUR_API_KEY_HERE with your actual Gemini API key

# 4. Run the server
python start.py
```

### Access the Application
- **🏠 Home**: http://localhost:8000
- **📊 Dashboard**: http://localhost:8000/static/dashboard.html
- **📚 API Docs**: http://localhost:8000/docs

**That's it!** Start testing scam detection and AI engagement in the dashboard.

## 📚 API Endpoints

### POST /detect
Detect if a message is a scam.
```json
{
  "message": "You won 10 lakh rupees! Send OTP to claim"
}
```

### POST /engage
Engage with scammer using AI persona.
```json
{
  "message": "Hello, this is regarding your bank account",
  "conversation_id": "optional-id"
}
```

### GET /intelligence/{conversation_id}
Retrieve extracted intelligence.

### GET /conversations
Get all conversation histories.

## 🛠️ Technology Stack

- **Backend**: FastAPI
- **AI/LLM**: Google Gemini API
- **Database**: SQLite
- **Frontend**: HTML/CSS/JavaScript

## 📝 Project Structure

```
scam-honeypot/
├── app/
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration
│   ├── models.py        # Pydantic models
│   └── database.py      # Database models
├── modules/
│   ├── scam_detector.py # Scam detection
│   ├── ai_agent.py      # AI persona
│   ├── intelligence.py  # Data extraction
│   └── personas.py      # Persona definitions
├── static/
│   └── dashboard.html   # Web dashboard
└── tests/
    └── test_scenarios.py
```

## 🎭 AI Personas

1. **Ramesh (68)** - Elderly, trusting, unfamiliar with technology
2. **Priya (35)** - Tech novice, cautious but curious
3. **Arjun (42)** - Eager investor, interested in quick returns

## 🔒 Security Note

This is a honeypot system designed for research and scam detection. Never use real personal information when testing.

## 📄 License

MIT License - Built for AI for Fraud Detection & User Safety Hackathon

## 👨‍💻 Author

Built with ❤️ for the hackathon
