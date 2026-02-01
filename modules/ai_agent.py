"""AI Agent with support for both Gemini and Groq APIs."""
import uuid
from typing import Dict, List, Optional
import google.generativeai as genai
from groq import Groq
from app import config
from modules.personas import PERSONAS, Persona
from modules.intelligence import IntelligenceExtractor


class AIAgent:
    """AI agent for engaging with scammers using personas."""
    
    def __init__(self):
        """Initialize AI agent with selected provider."""
        self.provider = config.Config.AI_PROVIDER
        self.conversations: Dict[str, Dict] = {}
        self.api_available = False
        
        if self.provider == "groq":
            self._init_groq()
        else:
            self._init_gemini()
    
    def _init_groq(self):
        """Initialize Groq API."""
        try:
            self.groq_client = Groq(api_key=config.Config.GROQ_API_KEY)
            self.api_available = True
            print("✅ Groq API initialized successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize Groq API: {e}")
            print("   Falling back to template responses")
            self.groq_client = None
            self.api_available = False
    
    def _init_gemini(self):
        """Initialize Gemini API."""
        try:
            genai.configure(api_key=config.Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(config.Config.GEMINI_MODEL)
            self.api_available = True
            print("✅ Gemini API initialized successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize Gemini API: {e}")
            print("   Falling back to template responses")
            self.model = None
            self.api_available = False
    
    def start_conversation(self, initial_message: str, persona_type: str = None) -> Dict:
        """
        Start a new conversation with a scammer.
        
        Args:
            initial_message: The scammer's initial message
            persona_type: Type of persona to use (elderly, tech_novice, eager_investor)
        
        Returns:
            Dict with conversation_id, response, persona, and extracted data
        """
        # Select persona
        if persona_type and persona_type in PERSONAS:
            persona = PERSONAS[persona_type]
        else:
            # Random persona selection
            import random
            persona = random.choice(list(PERSONAS.values()))
        
        # Create conversation
        conversation_id = str(uuid.uuid4())
        self.conversations[conversation_id] = {
            "persona": persona,
            "messages": [],
            "extracted_intelligence": []
        }
        
        # Add scammer's message
        self.conversations[conversation_id]["messages"].append({
            "role": "scammer",
            "content": initial_message
        })
        
        # Generate response
        response = self._generate_response(conversation_id, initial_message, persona)
        
        # Add AI response
        self.conversations[conversation_id]["messages"].append({
            "role": "agent",
            "content": response
        })
        
        # Extract intelligence from scammer's message
        extractor = IntelligenceExtractor()
        extracted = extractor.extract(initial_message, conversation_id)
        if extracted:
            self.conversations[conversation_id]["extracted_intelligence"].extend(extracted)
        
        return {
            "conversation_id": conversation_id,
            "response": response,
            "persona": persona.name,
            "extracted_data": extracted
        }
    
    def continue_conversation(self, conversation_id: str, message: str) -> Dict:
        """
        Continue an existing conversation.
        
        Args:
            conversation_id: ID of the conversation
            message: New message from scammer
        
        Returns:
            Dict with response and extracted data
        """
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        conv = self.conversations[conversation_id]
        persona = conv["persona"]
        
        # Add scammer's message
        conv["messages"].append({
            "role": "scammer",
            "content": message
        })
        
        # Generate response
        response = self._generate_response(conversation_id, message, persona)
        
        # Add AI response
        conv["messages"].append({
            "role": "agent",
            "content": response
        })
        
        # Extract intelligence
        extractor = IntelligenceExtractor()
        extracted = extractor.extract(message, conversation_id)
        if extracted:
            conv["extracted_intelligence"].extend(extracted)
        
        return {
            "conversation_id": conversation_id,
            "response": response,
            "persona": persona.name,
            "extracted_data": extracted
        }
    
    def _generate_response(self, conversation_id: str, message: str, persona: Persona) -> str:
        """Generate AI response using selected provider."""
        # If API not available, use fallback
        if not self.api_available:
            return self._get_fallback_response(persona, message)
        
        conv = self.conversations[conversation_id]
        
        # Build conversation history for context
        history = "\n".join([
            f"{'Scammer' if msg['role'] == 'scammer' else persona.name}: {msg['content']}"
            for msg in conv["messages"][-5:]  # Last 5 messages for context
        ])
        
        # Create prompt with persona and context
        prompt = f"""{persona.system_prompt}

CONVERSATION HISTORY:
{history}

SCAMMER'S LATEST MESSAGE:
{message}

YOUR TASK:
Respond naturally as {persona.name}. Your goal is to:
1. Keep the scammer engaged in conversation
2. Ask questions that might reveal their bank account, UPI ID, phone number, or links
3. Show appropriate curiosity or concern based on your persona
4. Gradually build trust so they share more information
5. Stay completely in character

IMPORTANT GUIDELINES:
- Keep responses short (2-3 sentences)
- Sound natural and human
- Show appropriate emotion for your persona
- Ask one relevant question to keep conversation going
- If they ask for money/OTP, show hesitation but don't refuse immediately

YOUR RESPONSE (as {persona.name}):"""
        
        try:
            if self.provider == "groq":
                return self._generate_groq_response(prompt)
            else:
                return self._generate_gemini_response(prompt)
        except Exception as e:
            print(f"⚠️  Error generating response: {e}")
            print("   Using fallback response")
            return self._get_fallback_response(persona, message)
    
    def _generate_groq_response(self, prompt: str) -> str:
        """Generate response using Groq API."""
        response = self.groq_client.chat.completions.create(
            model=config.Config.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.Config.GROQ_TEMPERATURE,
            max_tokens=config.Config.GROQ_MAX_TOKENS,
        )
        return response.choices[0].message.content.strip()
    
    def _generate_gemini_response(self, prompt: str) -> str:
        """Generate response using Gemini API."""
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": config.Config.GEMINI_TEMPERATURE,
                "max_output_tokens": config.Config.GEMINI_MAX_TOKENS,
            }
        )
        return response.text.strip()
    
    def _get_fallback_response(self, persona: Persona, message: str) -> str:
        """Generate fallback response when API is unavailable."""
        message_lower = message.lower()
        
        # Persona-specific fallback responses
        if persona.name == "Ramesh Kumar":
            if any(word in message_lower for word in ["otp", "password", "pin"]):
                return "What is this OTP you're asking for? My grandson told me never to share such things. But you're from the bank, right?"
            elif any(word in message_lower for word in ["account", "blocked", "suspended"]):
                return "Oh dear! My account is blocked? I'm very worried. What should I do? I'm not good with these computer things."
            elif any(word in message_lower for word in ["money", "transfer", "payment"]):
                return "Transfer money? I need to ask my son about this. How much do I need to send? Where should I send it?"
            else:
                return "I don't understand all this technology. Can you explain it simply? I'm 68 years old and these things confuse me."
        
        elif persona.name == "Priya Sharma":
            if any(word in message_lower for word in ["otp", "password", "pin"]):
                return "Hmm, I'm not sure about sharing OTP. How do I know you're really from the company? Can you verify?"
            elif any(word in message_lower for word in ["account", "blocked", "suspended"]):
                return "My account is blocked? That's strange. I just used it yesterday. Can you tell me more about what happened?"
            elif any(word in message_lower for word in ["money", "transfer", "payment"]):
                return "Why do I need to transfer money? This seems unusual. Can you give me your official contact number?"
            else:
                return "I want to help, but I need to verify this first. Can you provide some official documentation?"
        
        elif persona.name == "Arjun Mehta":
            if any(word in message_lower for word in ["invest", "profit", "return"]):
                return "Interesting! What's the expected ROI? How quickly can I see returns? Is there a minimum investment?"
            elif any(word in message_lower for word in ["money", "transfer", "payment"]):
                return "Sure, I'm interested. Where should I transfer the money? Do you accept UPI or bank transfer?"
            elif any(word in message_lower for word in ["opportunity", "scheme", "plan"]):
                return "Tell me more about this opportunity. How many people have already invested? What's the success rate?"
            else:
                return "I'm always looking for good investment opportunities. What are the details? How do I get started?"
        
        # Default fallback
        return "I see. Can you tell me more about this? I want to make sure I understand correctly."
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Get conversation details."""
        return self.conversations.get(conversation_id)
    
    def get_all_conversations(self) -> List[Dict]:
        """Get all conversations summary."""
        return [
            {
                "conversation_id": conv_id,
                "persona": conv["persona"].name,
                "message_count": len(conv["messages"]),
                "intelligence_count": len(conv["extracted_intelligence"])
            }
            for conv_id, conv in self.conversations.items()
        ]


# Create global instance
ai_agent = AIAgent()
