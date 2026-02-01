"""Quick start script to run the Scam Honeypot server."""
import sys
import os

def check_env():
    """Check if .env file exists and has API key."""
    if not os.path.exists('.env'):
        print("\n" + "="*60)
        print("❌ ERROR: .env file not found!")
        print("="*60)
        print("Please create a .env file with your Gemini API key:")
        print("1. Copy .env.example to .env")
        print("2. Get API key from: https://makersuite.google.com/app/apikey")
        print("3. Add it to .env file")
        print("="*60 + "\n")
        return False
    
    # Check if API key is configured
    with open('.env', 'r') as f:
        content = f.read()
        if 'PASTE_YOUR_API_KEY_HERE' in content:
            print("\n" + "="*60)
            print("⚠️  WARNING: Please configure your Gemini API key!")
            print("="*60)
            print("1. Open .env file")
            print("2. Replace PASTE_YOUR_API_KEY_HERE with your actual key")
            print("3. Get key from: https://makersuite.google.com/app/apikey")
            print("="*60 + "\n")
            return False
    
    return True

def main():
    """Main entry point."""
    print("\n🕵️  Starting Scam Honeypot Server...\n")
    
    if not check_env():
        sys.exit(1)
    
    try:
        import uvicorn
        from app.main import app
        
        print("✅ Configuration validated")
        print("✅ Starting server on http://localhost:8000")
        print("\n📊 Dashboard: http://localhost:8000/static/dashboard.html")
        print("📚 API Docs: http://localhost:8000/docs\n")
        
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
        print("\nMake sure you have installed dependencies:")
        print("  pip install -r requirements.txt\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
