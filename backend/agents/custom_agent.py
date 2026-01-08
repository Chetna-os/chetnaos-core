# backend/agents/custom_agent.py
"""
A templated agent for client-specific customizations.
Extend this for client-specific domain logic.
"""

import time
from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class CustomAgent(BaseAgent):
    """
    Custom agent for general conversational intelligence.
    Implements BaseAgent.handle() interface.
    """

    def __init__(self, client_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(name="CustomAgent", client_id=client_id, config=config)

    async def handle(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Default conversational intelligence agent.
        Always returns dict with "response" field (BaseAgent requirement).
        """
        context = context or {}

        # 🧠 TEMP BASIC INTELLIGENCE (no LLM yet)
        if "business" in text.lower():
            reply = (
                "Aap apne business ko grow karne ke liye 3 cheezon par focus karein:\n"
                "1. Customer problem clearly samjhein\n"
                "2. Repeatable sales process banayein\n"
                "3. Automation aur AI tools ka use karein"
            )
        else:
            reply = f"Aapne kaha: {text}"

        # BaseAgent expects "response" field, but we also add "reply" for consistency
        return {
            "response": reply,
            "reply": reply  # Alias for easier extraction
        }
