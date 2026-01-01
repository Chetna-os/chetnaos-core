# backend/trinetra/perception/text_sensors.py
import re
from typing import Dict

class TextSensor:
    """
    Lightweight text preprocessor and extractor.
    """
    def __init__(self):
        # simple stopwords; extend as needed
        self.stopwords = {"the","is","in","at","a","an","and","or","please"}

    def preprocess(self, text: str) -> str:
        if not text:
            return ""
        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        return text

    def extract_entities(self, text: str) -> Dict[str, str]:
        """Very simple entity heuristics (demo)."""
        out = {}
        if "price" in text.lower() or "kitna" in text.lower():
            out["intent"] = "price_inquiry"
        if "book" in text.lower() or "booking" in text.lower():
            out["intent"] = "booking"
        return out
