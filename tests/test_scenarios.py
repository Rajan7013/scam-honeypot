"""Test scenarios for the scam honeypot system."""

# Test messages for scam detection
TEST_SCAM_MESSAGES = [
    # UPI Fraud
    "Congratulations! You won 10 lakh rupees. Send OTP to claim prize.",
    "Your Paytm account has been blocked. Verify now by sharing OTP.",
    "Hello sir, I am from PhonePe support. Please share your UPI PIN.",
    
    # Bank Phishing
    "Your bank account will be suspended. Click here to verify: bit.ly/verify123",
    "RBI notice: Update your KYC details immediately or account will be closed.",
    "Your debit card has been blocked. Call 9876543210 to activate.",
    
    # Lottery Scam
    "You are selected as lucky draw winner! Claim 50 lakh prize now.",
    "Congratulations! You won iPhone 15 in Amazon lottery. Pay 500 delivery fee.",
    
    # Investment Fraud
    "Invest 5000, get 50000 in 7 days. Guaranteed returns. Limited slots.",
    "Join our crypto scheme. Double your money in 24 hours. WhatsApp: 9999999999",
    
    # OTP Scam
    "Your OTP is 123456. Do not share with anyone. - From Bank",
    "Verify your account by entering this OTP: 789012",
    
    # Legitimate Messages (should NOT be detected as scam)
    "Hi, how are you doing today?",
    "Meeting scheduled for tomorrow at 3 PM.",
    "Can you send me the project report?",
]

# Test conversation scenarios
CONVERSATION_SCENARIOS = {
    "upi_fraud": [
        "Hello sir, I am calling from Paytm customer care. Your account has some issue.",
        "We need to verify your account. Can you share your registered mobile number?",
        "Thank you. Now please share the OTP we just sent to your phone.",
        "Also, what is your UPI PIN for verification?",
        "Great! Your account is now verified. Transfer 100 rupees to 9876543210@paytm to activate premium features.",
    ],
    
    "bank_phishing": [
        "This is urgent message from your bank. Your account will be blocked in 24 hours.",
        "You need to update your KYC details immediately.",
        "Click this link to update: bit.ly/kyc-update-urgent",
        "Or call our customer care at 1800-123-4567",
        "Please share your account number and IFSC code for verification.",
    ],
    
    "investment_scam": [
        "Hello! I have an amazing investment opportunity for you.",
        "Invest just 10,000 rupees and get 1 lakh in 30 days. Guaranteed!",
        "Many people have already earned lakhs. This is 100% safe and legal.",
        "Just transfer money to my account: 123456789012 (HDFC Bank)",
        "Or you can use UPI: investor@paytm. Very simple and fast!",
    ]
}

# Expected extractions for testing
EXPECTED_EXTRACTIONS = {
    "bank_account": ["123456789012", "9876543210123"],
    "upi_id": ["9876543210@paytm", "investor@paytm"],
    "phone": ["9876543210", "1800-123-4567"],
    "url": ["bit.ly/verify123", "bit.ly/kyc-update-urgent"],
}

if __name__ == "__main__":
    print("Test Scenarios for Scam Honeypot")
    print("=" * 50)
    print(f"\nTotal test messages: {len(TEST_SCAM_MESSAGES)}")
    print(f"Conversation scenarios: {len(CONVERSATION_SCENARIOS)}")
    print("\nRun the server and use these messages in the dashboard!")
