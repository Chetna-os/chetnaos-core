from datetime import datetime


class FallbackReflection:
    """
    Stores WHY fallback happened.
    No self-justifying narratives allowed.
    """

    def reflect(self, fallback_event: dict) -> dict:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "reflection": {
                "what_happened": fallback_event.get("reason", []),
                "lesson": "Boundary reached — system chose safety.",
                "allowed_next_step": "Human review required"
            }
        }
