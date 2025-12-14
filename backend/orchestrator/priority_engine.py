from typing import Dict, Any


class PriorityEngine:
    """
    Decides which intent has higher execution priority.
    """

    def __init__(self):
        self.priority_order = {
            "support": 1,
            "goal": 2,
            "sales": 3,
            "lead": 4,
            "chat": 5,
            "custom": 6
        }

    def get_priority(self, intent: str) -> int:
        return self.priority_order.get(intent, 5)

    def score(self, intent: str, context: Dict[str, Any]) -> int:
        """
        Return a priority score for the given intent.
        """
        return self.get_priority(intent)

    def compare(self, intent_a: str, intent_b: str) -> str:
        """
        Returns higher priority intent.
        """
        if self.get_priority(intent_a) < self.get_priority(intent_b):
            return intent_a
        return intent_b
