# backend/agents/custom_agent.py
"""
A templated agent for client-specific customizations.
Extend this for client-specific domain logic.
"""

import time
from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, client_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(name="CustomAgent", client_id=client_id, config=config)

    async def handle(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Example: return concordant reply + echo metadata
        context = context or {}
        # You may add custom intent detection & routing here
        reply = f"CustomAgent: Received your message ({text[:120]}...)"
        # Example: store last user message
        self.update_state("last_message", {"text": text, "ts": time.time()})
        return {"response": reply, "meta": {"input_length": len(text), "context_keys": list(context.keys())}}
