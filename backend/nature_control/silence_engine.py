class SilenceEngine:
    """
  Pauses responses when confidence is low or ambiguity is high.
  """

    def __init__(self, min_confidence: float = 0.35):
        self.min_confidence = min_confidence

    def should_pause(self, confidence: float) -> bool:
        return confidence < self.min_confidence

    def pause_response(self) -> dict:
        return {
            "status":
            "paused",
            "reason":
            "low_confidence",
            "message":
            "Main is par thoda ruk kar sochna chahta hoon. Kripya thoda context dein ya baad me try karein."
        }
