# backend/billing/payments.py

from datetime import datetime
from typing import Dict


class PaymentService:
    """
    Handles payment status and records.
    """

    def _init_(self):
        # invoice_id -> payment info
        self.payments: Dict[str, Dict] = {}

    def mark_paid(
        self,
        invoice_id: str,
        method: str = "manual",
        reference: str = ""
    ):
        self.payments[invoice_id] = {
            "status": "paid",
            "method": method,
            "reference": reference,
            "paid_at": datetime.utcnow().isoformat(),
        }

    def mark_failed(self, invoice_id: str, reason: str):
        self.payments[invoice_id] = {
            "status": "failed",
            "reason": reason,
            "updated_at": datetime.utcnow().isoformat(),
        }

    def get_payment_status(self, invoice_id: str) -> Dict:
        return self.payments.get(
            invoice_id,
            {"status": "unpaid"}
        )
