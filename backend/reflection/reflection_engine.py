from typing import Dict, Any
import logging


logger = logging.getLogger("ReflectionEngine")


class ReflectionEngine:
    """
    Records and reflects on agent experiences.
    """

    def __init__(self):
        self.history = []

    def record(
        self,
        user_input: str,
        intent: str,
        output: Dict[str, Any],
        context: Dict[str, Any]
    ):
        """
        Record an experience for future reflection.
        """
        entry = {
            "user_input": user_input,
            "intent": intent,
            "output": output,
            "trace_id": context.get("trace_id")
        }
        self.history.append(entry)
        logger.info(f"Recorded experience: {intent}")

    def reflect(self, action: str, outcome: dict) -> dict:
        return {
            "action": action,
            "success": outcome.get("success", False),
            "lesson": outcome.get("lesson", "No lesson extracted"),
        }
