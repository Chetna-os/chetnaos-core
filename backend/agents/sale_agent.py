# backend/agents/sale_agent.py
"""
SalesAgent:
 - Template responses (config-driven)
 - Intent simple detection (keywords)
 - LLM hook is abstracted (so you can plug Groq/OpenAI later)
"""

import os
import asyncio
from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent

# Optional LLM hook: you may implement real call in integrations/llm.py
async def llm_call_stub(prompt: str, max_tokens: int = 300) -> str:
    # cheap stub (non-blocking)
    await asyncio.sleep(0.05)
    return f"[LLM-STUB] I understood: {prompt[:200]}"

class SalesAgent(BaseAgent):
    DEFAULT_TEMPLATES = {
        "greeting": "Namaste 🙏! Kaise madad kar sakta hoon? Aap kis project mein interest rakhte hain?",
        "price": "Hamare plots ₹{min_price} se start hote hain. Kya aapko brochure chahiye?",
        "location": "Project location: {address}. {distance} se Pune.",
        "booking": "Booking ke liye token ₹{token}. Mai site-visit arrange kar doon?",
        "fallback": "Aapka sawaal interesting hai — thoda aur bataiye ya mai sales team se connect kar doon."
    }

    def __init__(self, client_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(name="SalesAgent", client_id=client_id, config=config)
        self.templates = {**self.DEFAULT_TEMPLATES, **(self.config.get("templates", {}) or {})}
        self.keywords = {
            "price": ["price", "kitna", "cost", "costs", "rate", "price?"],
            "location": ["location", "kahaan", "address", "where"],
            "booking": ["book", "booking", "buy", "purchase", "interested"]
        }

    def _detect_intent(self, text: str) -> str:
        t = text.lower()
        for intent, kws in self.keywords.items():
            for k in kws:
                if k in t:
                    return intent
        if any(x in t for x in ["hi", "hello", "namaste"]):
            return "greeting"
        return "general"

    def _render_template(self, template_name: str) -> str:
        info = self.config.get("project_info", {})
        template = self.templates.get(template_name) or self.templates["fallback"]
        try:
            return template.format(
                min_price=info.get("min_price", "25 Lakhs"),
                max_price=info.get("max_price", "1 Crore"),
                address=info.get("address", "Pune - Nashik Highway"),
                distance=info.get("distance", "45 min from Pune"),
                token=info.get("token", "1 Lakh"),
            )
        except Exception:
            return self.templates["fallback"]

    async def _llm_enhanced_response(self, text: str, history: List[Dict[str, Any]]) -> str:
        # build a concise prompt
        prompt = f"Context: {self.config.get('project_info', {})}\nHistory: {history[-5:]}\nUser: {text}"
        # call integration - replace with real implementation later
        return await llm_call_stub(prompt)

    async def handle(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        intent = self._detect_intent(text)
        if intent in ["greeting", "price", "location", "booking"]:
            reply = self._render_template(intent)
        else:
            # compose using LLM for general queries
            history = self.get_state("conversation") or []
            reply = await self._llm_enhanced_response(text, history)
        # update conversation state
        conv = self.get_state("conversation") or []
        conv.append({"role": "user", "text": text})
        conv.append({"role": "agent", "text": reply})
        self.update_state("conversation", conv[-20:])  # keep last 20
        # simple lead scoring (example)
        lead_score = sum(10 for kw in ["book","buy","interested","visit","price"] if kw in text.lower())
        return {"response": reply, "intent": intent, "lead_score": min(100, lead_score)}
