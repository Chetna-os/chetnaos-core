class IntentDetector:
    """
    Detects user intent from incoming text.
    """

    def __init__(self):
        self.intent_map = {
            "sales": ["price", "cost", "buy", "purchase", "book", "investment"],
            "goal": ["goal", "target", "automate", "achieve"],
            "support": ["help", "issue", "problem", "error"],
            "lead": ["lead", "contact", "prospect"],
            "chat": ["hi", "hello", "namaste", "how", "what", "who"]
        }

    def detect(self, text: str) -> str:
        if not text:
            return "chat"

        text = text.lower()

        for intent, keywords in self.intent_map.items():
            for word in keywords:
                if word in text:
                    return intent

        return "custom"