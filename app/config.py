"""Configuration management for the Scam Honeypot system."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    HACKATHON_API_KEY = os.getenv("HACKATHON_API_KEY", "your-secret-api-key-here")
    
    # AI Provider Selection (groq or gemini)
    AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")  # Default to Groq
    
    # Mock Scammer API
    MOCK_SCAMMER_API_URL = os.getenv("MOCK_SCAMMER_API_URL", "")
    
    # Application Settings
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # Database
    DATABASE_URL = "sqlite:///./scam_honeypot.db"
    
    
    # Gemini Model Settings
    GEMINI_MODEL = "gemini-2.5-flash"
    GEMINI_TEMPERATURE = 0.7
    GEMINI_MAX_TOKENS = 500
    
    # Groq Model Settings
    GROQ_MODEL = "llama-3.3-70b-versatile"  # Fast and powerful
    GROQ_TEMPERATURE = 0.7
    GROQ_MAX_TOKENS = 500
    
    # Scam Detection Thresholds
    SCAM_CONFIDENCE_THRESHOLD = 0.6
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if cls.AI_PROVIDER == "gemini":
            if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == "PASTE_YOUR_API_KEY_HERE":
                print("\n" + "="*60)
                print("⚠️  WARNING: GEMINI_API_KEY not configured!")
                print("="*60)
                print("Please follow these steps:")
                print("1. Get API key from: https://makersuite.google.com/app/apikey")
                print("2. Open .env file in the project root")
                print("3. Replace PASTE_YOUR_API_KEY_HERE with your actual key")
                print("4. Restart the server")
                print("="*60 + "\n")
                raise ValueError("GEMINI_API_KEY is required. Please set it in .env file")
        elif cls.AI_PROVIDER == "groq":
            if not cls.GROQ_API_KEY or cls.GROQ_API_KEY == "PASTE_YOUR_GROQ_KEY_HERE":
                print("\n" + "="*60)
                print("⚠️  WARNING: GROQ_API_KEY not configured!")
                print("="*60)
                print("Please follow these steps:")
                print("1. Get FREE API key from: https://console.groq.com/keys")
                print("2. Open .env file in the project root")
                print("3. Add: GROQ_API_KEY=your_key_here")
                print("4. Restart the server")
                print("="*60 + "\n")
                raise ValueError("GROQ_API_KEY is required. Please set it in .env file")
        return True

config = Config()
