"""Scam detection module using pattern matching and AI analysis."""
import re
from typing import Tuple, Optional
from app.config import config

class ScamDetector:
    """Scam detection using keyword matching and pattern analysis."""
    
    # Scam keywords by category
    SCAM_KEYWORDS = {
        "urgency": [
            "urgent", "immediately", "now", "hurry", "quick", "fast",
            "limited time", "expires", "last chance", "act now"
        ],
        "financial": [
            "won", "prize", "lottery", "reward", "cashback", "refund",
            "crore", "lakh", "thousand", "money", "amount", "payment"
        ],
        "verification": [
            "verify", "confirm", "update", "validate", "authenticate",
            "otp", "password", "pin", "cvv", "account number", "card"
        ],
        "threats": [
            "blocked", "suspended", "deactivated", "closed", "terminated",
            "legal action", "police", "arrest", "fine", "penalty"
        ],
        "authority": [
            "bank", "rbi", "government", "income tax", "police",
            "customer care", "support team", "official", "department"
        ],
        "action_required": [
            "click", "link", "download", "install", "share", "forward",
            "call", "whatsapp", "message", "reply", "send"
        ]
    }
    
    # Scam type patterns
    SCAM_TYPES = {
        "upi_fraud": ["upi", "paytm", "phonepe", "gpay", "bhim"],
        "bank_phishing": ["account", "debit card", "credit card", "netbanking", "ifsc"],
        "lottery_scam": ["won", "lottery", "prize", "lucky draw", "winner"],
        "otp_scam": ["otp", "one time password", "verification code"],
        "investment_fraud": ["invest", "returns", "profit", "scheme", "double"]
    }
    
    def __init__(self):
        """Initialize scam detector."""
        self.confidence_threshold = config.SCAM_CONFIDENCE_THRESHOLD
    
    def detect(self, message: str) -> Tuple[bool, float, Optional[str], str]:
        """
        Detect if message is a scam.
        
        Returns:
            (is_scam, confidence, scam_type, explanation)
        """
        message_lower = message.lower()
        
        # Count keyword matches
        keyword_score = 0
        matched_categories = []
        
        for category, keywords in self.SCAM_KEYWORDS.items():
            matches = sum(1 for keyword in keywords if keyword in message_lower)
            if matches > 0:
                keyword_score += matches
                matched_categories.append(category)
        
        # Detect scam type
        scam_type = self._detect_scam_type(message_lower)
        
        # Calculate confidence (0-1 scale)
        # More keyword matches = higher confidence
        confidence = min(keyword_score / 10.0, 1.0)
        
        # Boost confidence if multiple categories matched
        if len(matched_categories) >= 3:
            confidence = min(confidence + 0.2, 1.0)
        
        # Check for suspicious patterns
        if self._has_suspicious_patterns(message):
            confidence = min(confidence + 0.15, 1.0)
        
        is_scam = confidence >= self.confidence_threshold
        
        # Generate explanation
        explanation = self._generate_explanation(
            is_scam, matched_categories, scam_type, confidence
        )
        
        return is_scam, confidence, scam_type, explanation
    
    def _detect_scam_type(self, message: str) -> Optional[str]:
        """Detect specific scam type."""
        for scam_type, keywords in self.SCAM_TYPES.items():
            if any(keyword in message for keyword in keywords):
                return scam_type
        return "generic_scam"
    
    def _has_suspicious_patterns(self, message: str) -> bool:
        """Check for suspicious patterns."""
        suspicious_patterns = [
            r'bit\.ly|tinyurl|goo\.gl',  # Shortened URLs
            r'\d{10,}',  # Long numbers (potential account numbers)
            r'click.*link|tap.*link',  # Click link requests
            r'congratulations.*won',  # Prize notifications
            r'verify.*account.*\d+',  # Account verification with numbers
        ]
        
        return any(re.search(pattern, message, re.IGNORECASE) 
                  for pattern in suspicious_patterns)
    
    def _generate_explanation(
        self, 
        is_scam: bool, 
        categories: list, 
        scam_type: Optional[str],
        confidence: float
    ) -> str:
        """Generate human-readable explanation."""
        if not is_scam:
            return "Message appears legitimate with low scam indicators."
        
        explanation_parts = [
            f"Detected as {scam_type or 'potential scam'} with {confidence:.0%} confidence."
        ]
        
        if categories:
            explanation_parts.append(
                f"Scam indicators: {', '.join(categories)}."
            )
        
        return " ".join(explanation_parts)

# Global instance
scam_detector = ScamDetector()
