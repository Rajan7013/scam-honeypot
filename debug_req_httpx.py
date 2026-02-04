import httpx
import json
import asyncio

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

async def test():
    try:
        print(f"Sending POST to {url}")
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
