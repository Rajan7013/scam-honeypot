"""Intelligence extraction module for extracting sensitive data from conversations."""
import re
from typing import List, Dict
from datetime import datetime

class IntelligenceExtractor:
    """Extract sensitive information from scammer messages."""
    
    # Extraction patterns
    PATTERNS = {
        "bank_account": r'\b\d{9,18}\b',
        "upi_id": r'\b[\w\.-]+@[\w\.-]+\b',
        "phone": r'(?:\+91[-\s]?)?[6-9]\d{9}',
        "url": r'https?://[^\s]+|(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}[^\s]*',
        "ifsc": r'\b[A-Z]{4}0[A-Z0-9]{6}\b',
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "pan": r'\b[A-Z]{5}\d{4}[A-Z]\b',
        "aadhaar": r'\b\d{4}\s?\d{4}\s?\d{4}\b'
    }
    
    def __init__(self):
        """Initialize intelligence extractor."""
        self.compiled_patterns = {
            key: re.compile(pattern, re.IGNORECASE)
            for key, pattern in self.PATTERNS.items()
        }
    
    def extract(self, message: str, conversation_id: str) -> List[Dict]:
        """
        Extract intelligence from message.
        
        Returns:
            List of extracted items with type, value, confidence
        """
        extracted = []
        
        for data_type, pattern in self.compiled_patterns.items():
            matches = pattern.findall(message)
            
            for match in matches:
                # Validate and calculate confidence
                confidence = self._calculate_confidence(data_type, match)
                
                if confidence > 0.5:  # Only include high-confidence matches
                    extracted.append({
                        "type": data_type,
                        "value": match.strip(),
                        "confidence": confidence,
                        "timestamp": datetime.utcnow(),
                        "conversation_id": conversation_id
                    })
        
        return extracted
    
    def _calculate_confidence(self, data_type: str, value: str) -> float:
        """Calculate confidence score for extracted data."""
        confidence = 0.7  # Base confidence
        
        # Type-specific validation
        if data_type == "bank_account":
            # Bank accounts are typically 9-18 digits
            if 9 <= len(value) <= 18:
                confidence = 0.9
            else:
                confidence = 0.6
        
        elif data_type == "upi_id":
            # UPI IDs must have @ symbol and valid format
            if "@" in value and len(value.split("@")) == 2:
                confidence = 0.95
            else:
                confidence = 0.5
        
        elif data_type == "phone":
            # Indian phone numbers start with 6-9
            clean_phone = re.sub(r'[^\d]', '', value)
            if len(clean_phone) == 10 and clean_phone[0] in '6789':
                confidence = 0.9
            else:
                confidence = 0.6
        
        elif data_type == "url":
            # URLs with common domains are more likely legitimate
            if any(domain in value.lower() for domain in ['bit.ly', 'tinyurl', 't.me']):
                confidence = 0.95  # Shortened URLs in scams
            else:
                confidence = 0.8
        
        elif data_type == "ifsc":
            # IFSC codes have specific format
            if len(value) == 11 and value[:4].isalpha():
                confidence = 0.95
            else:
                confidence = 0.6
        
        return confidence
    
    def extract_all_from_conversation(self, messages: List[str], conversation_id: str) -> List[Dict]:
        """Extract intelligence from entire conversation."""
        all_extracted = []
        
        for message in messages:
            extracted = self.extract(message, conversation_id)
            all_extracted.extend(extracted)
        
        # Remove duplicates
        unique_extracted = []
        seen = set()
        
        for item in all_extracted:
            key = (item["type"], item["value"])
            if key not in seen:
                seen.add(key)
                unique_extracted.append(item)
        
        return unique_extracted

# Global instance
intelligence_extractor = IntelligenceExtractor()
