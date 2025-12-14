from typing import Dict, Any


class CustomFlow:
    """
    Generic custom workflow handler.
    """

    def __init__(self, name="custom"):
        self.name = name
        self.steps = []

    def add_step(self, step_callable):
        self.steps.append(step_callable)

    def execute(
        self,
        user_input: str,
        intent: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the custom workflow.
        """
        return {
            "workflow": "custom",
            "message": f"Processed input: {user_input}",
            "intent": intent
        }
