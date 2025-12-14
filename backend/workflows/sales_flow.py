from typing import Dict, Any


class SalesFlow:
    """
    Sales-specific workflow handler.
    """

    def execute(
        self,
        user_input: str,
        intent: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the sales workflow.
        """
        score = context.get("lead_score", 50)

        if score >= 90:
            action = "close_now"
        elif score >= 70:
            action = "demo_call"
        else:
            action = "follow_up"

        return {
            "workflow": "sales",
            "action": action,
            "message": f"Sales flow executed for: {user_input}",
            "intent": intent
        }
