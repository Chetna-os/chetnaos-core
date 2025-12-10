class PriorityEngine:
    """
    Decides which intent has higher execution priority.
    """

    def _init_(self):
        self.priority_order = {
            "support": 1,
            "goal": 2,
            "sales": 3,
            "chat": 4
        }

    def get_priority(self, intent: str) -> int:
        return self.priority_order.get(intent, 5)

    def compare(self, intent_a: str, intent_b: str) -> str:
        """
        Returns higher priority intent.
        """
        if self.get_priority(intent_a) < self.get_priority(intent_b):
            return intent_a
        return intent_b
