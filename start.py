"""Server startup script for Hackathon Honey-Pot."""
import sys
import os
import uvicorn
from pathlib import Path

def check_env():
    """Check if API keys are set."""
    env_file = Path(".env")
    
    # 1. Check for Groq Key (The only one we strictly need)
    if os.getenv("GROQ_API_KEY"):
        print("✅ Using environment variables (cloud deployment)")
        return True
    
    # 2. Check for .env file (Local testing)
    if env_file.exists():
        print("✅ Found .env file")
        return True

    # 3. Fail if nothing found
    print("\n" + "="*60)
    print("❌ ERROR: GROQ_API_KEY not found!")
    print("="*60)
    print("Please set GROQ_API_KEY in your Render Dashboard")
    print("OR create a .env file for local development.")
    print("="*60 + "\n")
    return False

def main():
    """Main entry point."""
    print("\n🕵️  Starting Scam Honeypot Server...\n")
    
    # Stop if no keys
    if not check_env():
        sys.exit(1)
    
    try:
        print("✅ Configuration validated")
        print("✅ Starting server...")
        print("📚 API Docs: http://localhost:8000/docs\n")
        
        # NOTE: If your main.py is in a folder named 'app', keep "app.main:app"
        # If your main.py is in the ROOT folder, change this to "main:app"
        uvicorn.run(
            "app.main:app", 
            host="0.0.0.0",
            port=8000,
            reload=True
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()