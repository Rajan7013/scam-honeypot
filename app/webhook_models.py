"""Official hackathon webhook models."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class WebhookRequest(BaseModel):
    """Incoming webhook request from Mock Scammer API."""
    conversation_id: Optional[str] = None
    message: str
    timestamp: Optional[str] = None
    metadata: Optional[Dict] = None


class ExtractedIntelligence(BaseModel):
    """Structured intelligence data."""
    bank_accounts: List[str] = Field(default_factory=list)
    upi_ids: List[str] = Field(default_factory=list)
    phishing_urls: List[str] = Field(default_factory=list)
    phone_numbers: List[str] = Field(default_factory=list)
    ifsc_codes: List[str] = Field(default_factory=list)
    emails: List[str] = Field(default_factory=list)


class WebhookResponse(BaseModel):
    """Official hackathon response format."""
    scam_detected: bool
    confidence: float
    agent_engaged: bool
    conversation_turns: int
    extracted_intelligence: ExtractedIntelligence
    agent_response: str
    conversation_id: str
    agent_persona: Optional[str] = None
    scam_type: Optional[str] = None
