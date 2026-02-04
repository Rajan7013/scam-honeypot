"""
Test script to verify /hackathon/chat endpoint works exactly as GUVI expects.
This mimics the exact request format from the problem statement.
"""
import httpx
import asyncio
import json

# Configuration
API_URL = "https://scam-honeypot-8lfh.onrender.com/hackathon/chat"
API_KEY = "hackathon-secret-key-2026"

# Test Case 1: First Message (No conversation history)
test_payload_1 = {
    "sessionId": "test-session-12345",
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

# Test Case 2: Follow-up Message (With conversation history)
test_payload_2 = {
    "sessionId": "test-session-12345",
    "message": {
        "sender": "scammer",
        "text": "Share your UPI ID to avoid account suspension.",
        "timestamp": 1770005528731
    },
    "conversationHistory": [
        {
            "sender": "scammer",
            "text": "Your bank account will be blocked today. Verify immediately.",
            "timestamp": 1770005528731
        },
        {
            "sender": "user",
            "text": "Why will my account be blocked?",
            "timestamp": 1770005528731
        }
    ],
    "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    }
}

async def test_endpoint(payload, test_name):
    """Test the endpoint with given payload."""
    print(f"\n{'='*70}")
    print(f"🧪 TEST: {test_name}")
    print(f"{'='*70}")
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    print(f"\n📤 Sending Request:")
    print(f"URL: {API_URL}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(API_URL, json=payload, headers=headers)
            
            print(f"\n📥 Response:")
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Body: {response.text}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("status") == "success" and "reply" in data:
                        print(f"\n✅ TEST PASSED!")
                        print(f"AI Reply: {data['reply']}")
                        return True
                    else:
                        print(f"\n❌ TEST FAILED: Invalid response format")
                        return False
                except:
                    print(f"\n❌ TEST FAILED: Response is not valid JSON")
                    return False
            else:
                print(f"\n❌ TEST FAILED: Non-200 status code")
                return False
                
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def run_all_tests():
    """Run all test cases."""
    print("\n" + "="*70)
    print("🕵️ GUVI HACKATHON API ENDPOINT TESTER")
    print("="*70)
    
    results = []
    
    # Test 1: First message
    result1 = await test_endpoint(test_payload_1, "First Message (New Session)")
    results.append(("Test 1", result1))
    
    await asyncio.sleep(2)  # Wait between tests
    
    # Test 2: Follow-up message
    result2 = await test_endpoint(test_payload_2, "Follow-up Message (Existing Session)")
    results.append(("Test 2", result2))
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 TEST SUMMARY")
    print(f"{'='*70}")
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\n{'='*70}")
    if all_passed:
        print("🎉 ALL TESTS PASSED! Your API is ready for GUVI evaluation!")
    else:
        print("⚠️ SOME TESTS FAILED. Please review the errors above.")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    asyncio.run(run_all_tests())
