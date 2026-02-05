"""Module for reporting final results to the hackathon evaluation platform."""
import httpx
import logging
from typing import Dict, List, Optional
from app.config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HoneypotReporter:
    """Reporter for sending intelligence to hackathon callback endpoint."""
    
    CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    
    @staticmethod
    async def report_final_result(
        session_id: str,
        scam_detected: bool,
        total_messages: int,
        extracted_data: List[Dict],
        agent_notes: str = ""
    ) -> bool:
        """
        Send final result to evaluation endpoint.
        
        Args:
            session_id: Unique session ID provided by platform
            scam_detected: Boolean indicating if scam was detected
            total_messages: Total messages exchanged
            extracted_data: List of extracted intelligence dicts
            agent_notes: Summary notes from agent
            
        Returns:
            bool: True if reporting successful, False otherwise
        """
        try:
            # Format intelligence according to required schema
            intelligence_dict = {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "suspiciousKeywords": []
            }
            
            # Map internal types to required schema
            for item in extracted_data:
                item_type = item.get("type", "")
                value = item.get("value", "")
                
                if item_type == "bank_account":
                    intelligence_dict["bankAccounts"].append(value)
                elif item_type == "upi_id":
                    intelligence_dict["upiIds"].append(value)
                elif item_type == "url":
                    intelligence_dict["phishingLinks"].append(value)
                elif item_type == "phone":
                    intelligence_dict["phoneNumbers"].append(value)
            
            # Deduplicate lists
            for key in intelligence_dict:
                intelligence_dict[key] = list(set(intelligence_dict[key]))
            
            # Construct payload
            payload = {
                "sessionId": session_id,
                "scamDetected": scam_detected,
                "totalMessagesExchanged": total_messages,
                "extractedIntelligence": intelligence_dict,
                "agentNotes": agent_notes or "Scam intent detected and engaged autonomously."
            }
            
            logging.info(f"📤 Sending report to {HoneypotReporter.CALLBACK_URL}")
            logging.info(f"📦 Payload: {payload}")
            
            # Send async request
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    HoneypotReporter.CALLBACK_URL,
                    json=payload
                )
                
                if response.status_code == 200:
                    logging.info(f"✅ Report sent successfully: {response.text}")
                    return True
                else:
                    logging.error(f"❌ Failed to report result: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logging.error(f"❌ Error in report_final_result: {str(e)}")
            return False

# Global instance
reporter = HoneypotReporter()
