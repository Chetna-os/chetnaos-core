# backend/agents/whatsapp_agent.py
"""
WhatsAppAgent: formats message payloads suitable for WhatsApp channels.
This file does not directly call WhatsApp APIs; instead it returns a structured
payload that an integrations layer can send via Twilio/Meta API.
"""

from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent

class WhatsAppAgent(BaseAgent):
    def __init__(self, client_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(name="WhatsAppAgent", client_id=client_id, config=config)
        self.max_len = 4096

    def _format_quick_replies(self, options: List[str]) -> List[Dict[str, str]]:
        return [{"title": o[:20], "id": str(i)} for i, o in enumerate(options)]

    async def handle(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        ctx = context or {}
        # Basic command handling example
        if text.strip().startswith("/"):
            cmd = text.strip().lstrip("/")
            if cmd == "help":
                resp = "Commands: /help /brochure /visit"
                return {"response": resp, "whatsapp_payload": {"type": "text", "text": resp}}
        # Compose message
        # Use SalesAgent for core reply if integrated (example)
        reply_text = f"WhatsAppBot: {text[:200]}"
        quick = self._format_quick_replies(["Book site visit", "Request brochure", "Talk to sales"])
        payload = {
            "type": "text",
            "text": reply_text,
            "quick_replies": quick
        }
        # Return structured payload to be consumed by integrations layer
        return {"response": reply_text, "whatsapp_payload": payload}
