import httpx
import json
import time

# Test the exact request GUVI sends
url = "https://scam-honeypot-8lfh.onrender.com/hackathon/chat"
headers = {
    "x-api-key": "hackathon-secret-key-2026",
    "Content-Type": "application/json"
}

payload = {
    "sessionId": "test-urgent-fix",
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

print("🧪 Testing endpoint after timeout fix...")
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")

try:
    start = time.time()
    response = httpx.post(url, json=payload, headers=headers, timeout=30.0)
    elapsed = time.time() - start
    
    print(f"\n✅ Response received in {elapsed:.2f}s")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n🎉 SUCCESS! Endpoint is working!")
    else:
        print(f"\n❌ Error: {response.status_code}")
        
except httpx.TimeoutException:
    print("\n❌ TIMEOUT! Request took longer than 30 seconds")
except Exception as e:
    print(f"\n❌ Error: {e}")
