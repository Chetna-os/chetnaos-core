# backend/trinetra/perception/data_quality.py
from typing import Dict

class DataQualityChecker:
    """
    Basic checks: non-empty, length, suspicious tokens.
    Expandable with schema checks.
    """
    suspicious_tokens = ["<script>", "DROP TABLE", "eval("]

    def check(self, text: str) -> Dict[str, object]:
        if not text:
            return {"ok": False, "reason": "empty"}
        length = len(text)
        if any(tok.lower() in text.lower() for tok in self.suspicious_tokens):
            return {"ok": False, "reason": "suspicious_content"}
        if length < 3:
            return {"ok": False, "reason": "too_short"}
        return {"ok": True, "length": length}
