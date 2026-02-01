"""Autonomous agent worker for continuous scammer engagement."""
import asyncio
import httpx
from typing import Optional
from datetime import datetime
from app.config import config
from modules.ai_agent import ai_agent
from modules.scam_detector import scam_detector


class AutonomousAgent:
    """Autonomous agent that continuously engages with scammers."""
    
    def __init__(self):
        self.running = False
        self.active_conversations = {}
        self.poll_interval = 10  # seconds
        self.max_messages_per_conversation = 20
        
    async def start(self):
        """Start the autonomous agent."""
        self.running = True
        print("🤖 Autonomous Agent started - monitoring for scammers...")
        
        while self.running:
            try:
                await self._poll_and_engage()
                await asyncio.sleep(self.poll_interval)
            except Exception as e:
                print(f"⚠️  Agent error: {e}")
                await asyncio.sleep(self.poll_interval)
    
    def stop(self):
        """Stop the autonomous agent."""
        self.running = False
        print("🛑 Autonomous Agent stopped")
    
    async def _poll_and_engage(self):
        """Poll for new scammer messages and engage automatically."""
        # Check if Mock Scammer API is configured
        if not config.MOCK_SCAMMER_API_URL or \
           config.MOCK_SCAMMER_API_URL == "https://mock-scammer-api.example.com":
            # No external API - simulate scammer messages for demo
            await self._simulate_scammer_engagement()
            return
        
        # Poll Mock Scammer API for new messages
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{config.MOCK_SCAMMER_API_URL}/messages",
                    timeout=5.0
                )
                
                if response.status_code == 200:
                    messages = response.json()
                    for msg in messages:
                        await self._handle_scammer_message(msg)
        except Exception as e:
            print(f"⚠️  Failed to poll Mock API: {e}")
    
    async def _simulate_scammer_engagement(self):
        """Simulate scammer engagement for demo purposes."""
        # This runs when no external Mock API is available
        # It demonstrates the autonomous capability
        
        # Check if we have any active simulated conversations
        if len(self.active_conversations) == 0:
            # Start a new simulated conversation every 30 seconds
            current_time = datetime.now().timestamp()
            if not hasattr(self, '_last_sim_time'):
                self._last_sim_time = 0
            
            if current_time - self._last_sim_time > 30:
                self._last_sim_time = current_time
                await self._start_simulated_conversation()
        
        # Continue existing conversations
        for conv_id in list(self.active_conversations.keys()):
            conv = self.active_conversations[conv_id]
            
            # Check if conversation should continue
            if conv['message_count'] >= self.max_messages_per_conversation:
                print(f"✅ Conversation {conv_id[:8]} completed ({conv['message_count']} messages)")
                del self.active_conversations[conv_id]
                continue
            
            # Generate next scammer message (simulated)
            scammer_msg = self._generate_simulated_scammer_response(conv)
            
            if scammer_msg:
                await self._respond_to_scammer(conv_id, scammer_msg)
    
    async def _start_simulated_conversation(self):
        """Start a new simulated conversation with a scammer."""
        # Simulated scammer opening messages
        scammer_openers = [
            "Hello sir, your bank account will be blocked. Please verify immediately.",
            "Congratulations! You won 10 lakh rupees. Click here to claim: bit.ly/prize123",
            "Dear customer, your KYC is pending. Update now or account suspended.",
            "Invest 5000 and get 50000 in 7 days. 100% guaranteed returns!",
            "Your OTP is 123456. Do not share with anyone. - SBI Bank",
        ]
        
        import random
        initial_message = random.choice(scammer_openers)
        
        # Detect if it's a scam
        is_scam, confidence, scam_type, _ = scam_detector.detect(initial_message)
        
        if is_scam and confidence > 0.7:
            # Start engagement
            result = ai_agent.start_conversation(initial_message)
            conv_id = result['conversation_id']
            
            self.active_conversations[conv_id] = {
                'message_count': 2,  # Initial message + first response
                'persona': result['persona'],
                'scam_type': scam_type,
                'started_at': datetime.now()
            }
            
            print(f"🎯 New scam detected: {scam_type}")
            print(f"🤖 Started conversation {conv_id[:8]} as {result['persona']}")
            print(f"   Scammer: {initial_message[:60]}...")
            print(f"   AI: {result['response'][:60]}...")
    
    def _generate_simulated_scammer_response(self, conv):
        """Generate a simulated scammer response based on conversation context."""
        # Simulated scammer responses based on scam type
        responses_by_type = {
            'phishing': [
                "Yes sir, please share your account number and OTP to verify.",
                "Your account will be blocked in 24 hours. Share details now.",
                "Click this link to update: bit.ly/update123",
            ],
            'lottery_scam': [
                "To claim your prize, pay 500 rupees processing fee to 9876543210@paytm",
                "Send your bank details to transfer 10 lakh rupees.",
                "Pay tax of 2000 rupees first. UPI: scammer@okaxis",
            ],
            'investment_scam': [
                "Minimum investment is 5000. Send to account 123456789012.",
                "Join our WhatsApp group for daily profits: wa.me/+919876543210",
                "Transfer money to IFSC: SBIN0001234, Account: 987654321098",
            ],
            'tech_support': [
                "Your computer has virus. Pay 3000 for removal.",
                "Download this software: malware.com/fix.exe",
                "Give me remote access to fix the issue.",
            ]
        }
        
        scam_type = conv.get('scam_type', 'phishing')
        import random
        
        # Get appropriate responses for this scam type
        possible_responses = responses_by_type.get(scam_type, responses_by_type['phishing'])
        
        # Return a random response
        return random.choice(possible_responses)
    
    async def _respond_to_scammer(self, conv_id, scammer_message):
        """Generate and send AI response to scammer."""
        try:
            # Generate AI response
            result = ai_agent.continue_conversation(conv_id, scammer_message)
            
            # Update conversation tracking
            self.active_conversations[conv_id]['message_count'] += 2
            
            # Log the exchange
            print(f"💬 Conversation {conv_id[:8]}:")
            print(f"   Scammer: {scammer_message[:60]}...")
            print(f"   AI ({result['persona']}): {result['response'][:60]}...")
            
            if result.get('extracted_data'):
                for item in result['extracted_data']:
                    print(f"   🎯 Extracted {item['type']}: {item['value']}")
            
            # If external API exists, send response back
            if config.MOCK_SCAMMER_API_URL and \
               config.MOCK_SCAMMER_API_URL != "https://mock-scammer-api.example.com":
                await self._send_response_to_api(conv_id, result['response'])
        
        except Exception as e:
            print(f"❌ Error responding to scammer: {e}")
    
    async def _send_response_to_api(self, conv_id, response):
        """Send AI response back to Mock Scammer API."""
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{config.MOCK_SCAMMER_API_URL}/respond",
                    json={
                        "conversation_id": conv_id,
                        "message": response
                    },
                    timeout=5.0
                )
        except Exception as e:
            print(f"⚠️  Failed to send response to API: {e}")
    
    async def _handle_scammer_message(self, message_data):
        """Handle incoming scammer message from external API."""
        conv_id = message_data.get('conversation_id')
        message = message_data.get('message')
        
        if not conv_id or not message:
            return
        
        # Check if this is a new conversation
        if conv_id not in self.active_conversations:
            # Detect if it's a scam
            is_scam, confidence, scam_type, _ = scam_detector.detect(message)
            
            if is_scam and confidence > 0.7:
                # Start new conversation
                result = ai_agent.start_conversation(message)
                self.active_conversations[conv_id] = {
                    'message_count': 2,
                    'persona': result['persona'],
                    'scam_type': scam_type,
                    'started_at': datetime.now()
                }
                
                # Send response
                await self._send_response_to_api(conv_id, result['response'])
        else:
            # Continue existing conversation
            await self._respond_to_scammer(conv_id, message)


# Global instance
autonomous_agent = AutonomousAgent()
