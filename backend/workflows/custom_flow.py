from backend.integrations.llm import LLMRegistry
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

    def execute(self, user_input: str, intent: str,
                context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the custom workflow using active LLM.
        """

        llm = LLMRegistry.get()  # 🔥 SINGLE SOURCE OF TRUTH

        prompt = f"""
    User Input: {user_input}
    Detected Intent: {intent}
    Context: {context}

    Respond helpfully and clearly.
    """

        response = llm.generate(prompt=prompt,
                                context=[{
                                    "role": "user",
                                    "content": user_input
                                }])

        return {
            "workflow": self.name,
            "llm_model": response.get("model"),
            "output": response.get("text"),
            "tokens_used": response.get("tokens_used"),
        }
