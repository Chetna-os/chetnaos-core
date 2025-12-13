# backend/billing/invoices.py

from datetime import datetime
from typing import Dict
from uuid import uuid4


class InvoiceService:
    """
    Generates invoices based on usage.
    """

    PRICE_PER_MESSAGE = 0.20   # ₹
    PRICE_PER_TOKEN = 0.01     # ₹
    PRICE_PER_AGENT_CALL = 2.0 # ₹

    def generate_invoice(self, client_id: str, usage: Dict) -> Dict:
        messages = usage.get("messages", 0)
        tokens = usage.get("tokens", 0)
        agent_calls = usage.get("agent_calls", 0)

        amount = (
            messages * self.PRICE_PER_MESSAGE
            + tokens * self.PRICE_PER_TOKEN
            + agent_calls * self.PRICE_PER_AGENT_CALL
        )

        invoice = {
            "invoice_id": str(uuid4()),
            "client_id": client_id,
            "messages": messages,
            "tokens": tokens,
            "agent_calls": agent_calls,
            "total_amount": round(amount, 2),
            "currency": "INR",
            "generated_at": datetime.utcnow().isoformat(),
            "status": "pending",
        }

        return invoice
