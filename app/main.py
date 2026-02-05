"""Main FastAPI application for Scam Honeypot."""
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
import logging
from datetime import datetime

from app import models, database, config
from app.models import (
    ScamDetectionRequest, ScamDetectionResponse,
    EngagementRequest, EngagementResponse,
    WebhookRequest, WebhookResponse,
    HackathonChatResponse
)

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title="Scam Honeypot API",
    description="AI-powered scam detection and engagement system",
    version="1.0.0"
)

# Enable CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database initialization
@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    database.init_db()
    print("✅ Database initialized successfully")

@app.get("/")
async def root():
    """Root endpoint - returns dashboard."""
    return {
        "message": "Scam Honeypot API",
        "version": "1.0.0",
        "endpoints": {
            "dashboard": "/static/dashboard.html",
            "docs": "/docs",
            "detect": "/detect",
            "engage": "/engage",
            "webhook": "/webhook",
            "hackathon_chat": "/hackathon/chat"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Import endpoints after app initialization to avoid circular imports
from modules.scam_detector import scam_detector
from modules.intelligence import IntelligenceExtractor

@app.post("/webhook", response_model=WebhookResponse)
async def webhook_handler(
    request: WebhookRequest,
    db: Session = Depends(database.get_db)
):
    """
    Main webhook endpoint for receiving scam messages.
    This is the primary entry point for the hackathon evaluation.
    """
    from modules.ai_agent import ai_agent
    from modules.reporting import reporter
    
    try:
        # Step 1: Detect scam
        detection_result = scam_detector.detect(request.message)
        is_scam = detection_result["is_scam"]
        confidence = detection_result["confidence"]
        scam_type = detection_result.get("scam_type", "unknown")
        
        # Step 2: If scam detected, engage with AI agent
        agent_engaged = False
        agent_response = ""
        conversation_id = None
        persona = None
        conversation_turns = 0
        
        if is_scam:
            # Start or continue conversation
            result = ai_agent.start_conversation(request.message)
            agent_engaged = True
            agent_response = result["response"]
            conversation_id = result["conversation_id"]
            persona = result["persona"]
            conversation_turns = 1
        
        # Step 3: Extract intelligence
        extractor = IntelligenceExtractor()
        extracted = extractor.extract(request.message, conversation_id or "no-conversation")
        
        # Step 4: Build intelligence object
        intelligence = models.ExtractedIntelligence(
            upiIds=[],
            bankAccounts=[],
            phoneNumbers=[],
            phishingLinks=[],
            suspiciousKeywords=[],
            emails=[]
        )
        
        for item in extracted:
            value = item.get("value", "")
            intel_type = item.get("type", "")
            
            if intel_type == "upi_id":
                intelligence.upiIds.append(value)
            elif intel_type == "bank_account":
                intelligence.bankAccounts.append(value)
            elif intel_type == "phone":
                intelligence.phoneNumbers.append(value)
            elif intel_type == "url":
                intelligence.phishingLinks.append(value)
            elif intel_type == "keyword":
                intelligence.suspiciousKeywords.append(value)
            elif intel_type == "email":
                intelligence.emails.append(value)
        
        # Step 5: Return official format
        return WebhookResponse(
            scam_detected=is_scam,
            confidence=confidence,
            agent_engaged=agent_engaged,
            conversation_turns=conversation_turns,
            extracted_intelligence=intelligence,
            agent_response=agent_response,
            conversation_id=conversation_id,
            agent_persona=persona,
            scam_type=scam_type if is_scam else None
        )
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Error in /webhook endpoint: {str(e)}")
        print(f"   Full traceback:\n{error_details}")
        raise HTTPException(status_code=500, detail=f"Webhook error: {str(e)}")

from fastapi import Request

@app.post("/hackathon/chat", response_model=HackathonChatResponse)
async def hackathon_chat_handler(
    request: Request,
    x_api_key: Optional[str] = Header(None, alias="x-api-key")
):
    """
    Dedicated endpoint for the Hackathon Evaluation Platform.
    Accepts raw JSON to avoid validation errors.
    """
    # 1. Validate API Key
    if x_api_key != config.config.HACKATHON_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid X-API-Key")

    from modules.ai_agent import ai_agent
    import asyncio
    
    async def process_request():
        """Process the request with timeout protection."""
        try:
            # 2. Parse Raw JSON manually to be robust
            body = await request.json()
            print(f"📥 Received Hackathon Payload: {body}") # Log it!
            
            session_id = body.get("sessionId", "unknown_session")
            message_data = body.get("message", {})
            user_message = message_data.get("text", "")
            
            if not user_message:
                # Fallback if structure is different
                user_message = str(body)
                
            # 3. Handle Conversation
            # Check for existing session map
            if not hasattr(app, "session_map"):
                app.session_map = {}
                
            conversation_id = app.session_map.get(session_id)
            response_text = ""
            
            if conversation_id and conversation_id in ai_agent.conversations:
                result = ai_agent.continue_conversation(conversation_id, user_message, session_id=session_id)
                response_text = result["response"]
            else:
                result = ai_agent.start_conversation(user_message, session_id=session_id)
                conversation_id = result["conversation_id"]
                app.session_map[session_id] = conversation_id
                response_text = result["response"]
                
            return HackathonChatResponse(
                status="success",
                reply=response_text
            )
                
        except Exception as e:
            print(f"❌ Error in /hackathon/chat: {e}")
            # Return success with fallback message
            return HackathonChatResponse(status="success", reply="I'm not sure I understand. Can you explain what you mean?")
    
    try:
        # Wrap entire request processing in 25-second timeout
        return await asyncio.wait_for(process_request(), timeout=25.0)
    except asyncio.TimeoutError:
        print("⏱️  Request timed out after 25 seconds - returning fallback")
        return HackathonChatResponse(
            status="success",
            reply="Sorry, what was that? I didn't quite catch what you're saying. Can you repeat?"
        )


@app.get("/hackathon/chat", response_model=HackathonChatResponse)
async def hackathon_chat_get_handler():
    """Handle GET requests for connectivity checks."""
    return HackathonChatResponse(status="success", reply="System Online. Use POST for interaction.")


@app.post("/detect", response_model=ScamDetectionResponse)
async def detect_scam(request: ScamDetectionRequest):
    """Detect if a message is a scam."""
    from modules.scam_detector import scam_detector
    
    result = scam_detector.detect(request.message)
    
    return ScamDetectionResponse(
        is_scam=result["is_scam"],
        confidence=result["confidence"],
        scam_type=result.get("scam_type"),
        indicators=result.get("indicators", [])
    )

@app.post("/engage", response_model=EngagementResponse)
async def engage_scammer(request: EngagementRequest):
    """Engage with a scammer using AI agent."""
    from modules.ai_agent import ai_agent
    
    if request.conversation_id and request.conversation_id in ai_agent.conversations:
        # Continue existing conversation
        result = ai_agent.continue_conversation(request.conversation_id, request.message)
    else:
        # Start new conversation
        result = ai_agent.start_conversation(request.message, request.persona_type)
    
    return EngagementResponse(
        conversation_id=result["conversation_id"],
        response=result["response"],
        persona=result["persona"],
        extracted_data=result.get("extracted_data", [])
    )

@app.get("/conversations")
async def list_conversations():
    """List all active conversations."""
    from modules.ai_agent import ai_agent
    
    conversations = []
    for conv_id, conv_data in ai_agent.conversations.items():
        conversations.append({
            "conversation_id": conv_id,
            "persona": conv_data["persona"].name,
            "message_count": len(conv_data["messages"]),
            "intelligence_count": len(conv_data["extracted_intelligence"])
        })
    
    return {"conversations": conversations}

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get details of a specific conversation."""
    from modules.ai_agent import ai_agent
    
    if conversation_id not in ai_agent.conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conv = ai_agent.conversations[conversation_id]
    return {
        "conversation_id": conversation_id,
        "persona": {
            "name": conv["persona"].name,
            "age": conv["persona"].age,
            "occupation": conv["persona"].occupation
        },
        "messages": conv["messages"],
        "extracted_intelligence": conv["extracted_intelligence"]
    }

@app.get("/intelligence/{conversation_id}")
async def get_intelligence(conversation_id: str):
    """Get extracted intelligence for a specific conversation."""
    from modules.ai_agent import ai_agent
    
    if conversation_id not in ai_agent.conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return ai_agent.conversations[conversation_id]["extracted_intelligence"]

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the dashboard HTML."""
    with open("static/dashboard.html", "r") as f:
        return f.read()

@app.get("/stats")
async def get_stats():
    """Get system statistics."""
    from modules.ai_agent import ai_agent
    from modules.scam_detector import scam_detector
    
    total_conversations = len(ai_agent.conversations)
    total_intelligence = sum(
        len(conv["extracted_intelligence"]) 
        for conv in ai_agent.conversations.values()
    )
    
    return {
        "total_scans": scam_detector.total_scans,
        "scams_detected": scam_detector.scams_detected,
        "active_conversations": total_conversations,
        "intelligence_extracted": total_intelligence
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)