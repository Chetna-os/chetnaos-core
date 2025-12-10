# backend/agi/reflection_loop.py

from typing import Dict, Any
from datetime import datetime


class ReflectionLoop:
    """
    Learns from outcomes and updates AGI behavior.
    This is Self-Learning Loop.
    """

    def _init_(self):
        self.history = []

    def reflect(self, task: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        success = result.get("success", False)

        reflection = {
            "task": task,
            "result": result,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
            "adjustment": self._generate_adjustment(success)
        }

        self.history.append(reflection)
        return reflection

    def _generate_adjustment(self, success: bool) -> str:
        if success:
            return "increase_priority"
        return "change_strategy"

    def get_learning_history(self):
        return self.history[-20:]  # last 20 reflections only
