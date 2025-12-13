# backend/core/reasoning.py

class ReasoningEngine:
    def _init_(self):
        self.history = []

    def reason(self, context: dict, goal: str) -> dict:
        decision = {
            "goal": goal,
            "based_on": context,
            "action": f"analyze_{goal}",
            "confidence": 0.6
        }

        self.history.append(decision)
        return decision

    def get_reasoning_history(self):
        return self.history
