"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ScamDetectionRequest(BaseModel):
    """Request model for scam detection."""
    message: str = Field(..., description="Message to analyze for scam content")

class ScamDetectionResponse(BaseModel):
    """Response model for scam detection."""
    is_scam: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    scam_type: Optional[str] = None
    explanation: Optional[str] = None

class EngageRequest(BaseModel):
    """Request model for engaging with scammer."""
    message: str
    conversation_id: Optional[str] = None

class EngageResponse(BaseModel):
    """Response model for engagement."""
    response: str
    persona: str
    conversation_id: str
    extracted_data: List[dict] = []

class IntelligenceItem(BaseModel):
    """Model for extracted intelligence."""
    type: str  # bank_account, upi_id, phone, url, ifsc
    value: str
    confidence: float
    timestamp: datetime
    conversation_id: str

class IntelligenceResponse(BaseModel):
    """Response model for intelligence retrieval."""
    conversation_id: str
    bank_accounts: List[str] = []
    upi_ids: List[str] = []
    phones: List[str] = []
    urls: List[str] = []
    ifsc_codes: List[str] = []
    total_items: int

class ConversationMessage(BaseModel):
    """Model for a single conversation message."""
    role: str  # 'scammer' or 'agent'
    message: str
    timestamp: datetime

class ConversationHistory(BaseModel):
    """Model for conversation history."""
    conversation_id: str
    persona: str
    messages: List[ConversationMessage]
    intelligence_count: int
    started_at: datetime

# Hackathon Specific Models
class HackathonMessage(BaseModel):
    """Message format for hackathon platform."""
    sender: str  # 'scammer' or 'user'
    text: str
    timestamp: int

class HackathonMetadata(BaseModel):
    """Metadata for hackathon platform."""
    channel: Optional[str] = "SMS"
    language: Optional[str] = "English"
    locale: Optional[str] = "IN"

class HackathonChatRequest(BaseModel):
    """Request format from hackathon platform."""
    sessionId: str
    message: HackathonMessage
    conversationHistory: List[HackathonMessage] = []
    metadata: Optional[HackathonMetadata] = None

    class Config:
        extra = "ignore"

class HackathonChatResponse(BaseModel):
    """Response format expected by platform."""
    status: str
    reply: str
