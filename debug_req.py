import requests
import json

url = "http://localhost:8000/hackathon/chat"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "hackathon-secret-key-2026"
}

# Payload exactly from Problem Statement
payload = {
  "sessionId": "wertyu-dfghj-ertyui",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked today. Verify immediately.",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}

try:
    print(f"Sending POST to {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
