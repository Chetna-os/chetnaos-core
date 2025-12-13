class ReflectionEngine:
    def reflect(self, action: str, outcome: dict) -> dict:
        return {
            "action": action,
            "success": outcome.get("success", False),
            "lesson": outcome.get("lesson", "No lesson extracted"),
        }
