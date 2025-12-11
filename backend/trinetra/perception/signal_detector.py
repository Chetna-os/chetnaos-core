# backend/trinetra/perception/signal_detector.py
from typing import Dict, List

class SignalDetector:
    """
    Detects simple signals useful for triage (buying signal, urgency, sentiment stub).
    """
    BUYING_WORDS = {"buy","book","purchase","interested","visit","kitna"}
    URGENCY_WORDS = {"now","urgent","immediately","asap"}

    def detect(self, text: str) -> Dict[str, object]:
        t = text.lower()
        buying = any(w in t for w in self.BUYING_WORDS)
        urgency = any(w in t for w in self.URGENCY_WORDS)
        # naive sentiment stub:
        sentiment = "neutral"
        if "thank" in t or "thanks" in t:
            sentiment = "positive"
        if "not happy" in t or "bad" in t:
            sentiment = "negative"
        return {"buying": buying, "urgency": urgency, "sentiment": sentiment}
