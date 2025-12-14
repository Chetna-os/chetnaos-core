from typing import Dict, Any


class DharmaNet:
    """
    Validates actions against ethical/dharma rules.
    """

    def __init__(self):
        self.blocked_keywords = ["harm", "malicious", "illegal"]

    def validate(
        self,
        intent: str,
        priority: int,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check if the action is allowed based on dharma rules.
        """
        user_input = context.get("user_input", "").lower()

        for keyword in self.blocked_keywords:
            if keyword in user_input:
                return {
                    "allowed": False,
                    "reason": f"Blocked due to policy violation: {keyword}"
                }

        return {
            "allowed": True,
            "reason": None
        }
