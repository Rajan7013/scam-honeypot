import requests
import json

# Test local server
url = "http://127.0.0.1:8000/hackathon/chat"
headers = {
    "x-api-key": "hackathon-secret-key-2026",
    "Content-Type": "application/json"
}

payload = {
    "sessionId": "local-test-123",
    "message": {
        "sender": "scammer",
        "text": "Your SBI account is blocked. Verify KYC immediately.",
        "timestamp": 1770005528731
    },
    "conversationHistory": [],
    "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    }
}

print("🧪 Testing LOCAL endpoint...")
print(f"URL: {url}")

try:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    print(f"\n✅ Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"\n❌ Error: {e}")
