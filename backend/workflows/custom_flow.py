from backend.integrations.llm import LLMRegistry
from typing import Dict, Any


class CustomFlow:

    def __init__(self, name="custom"):
        self.name = name
        self.steps = []

    def add_step(self, step_callable):
        self.steps.append(step_callable)

    def execute(self, user_input: str, intent: str, context: dict):
        """
        Workflow NEVER decides.
        It only executes when BrainRouter allows.
        """

        llm = LLMRegistry.get()  # single source of truth

        prompt = f"""
        User Input: {user_input}
        Detected Intent: {intent}
        Context: {context}
        """

        response = llm.generate(prompt)

        return {
            "workflow": self.name,
            "status": "completed",
            "output": response,
            "trace_id": context.get("wisdom", {}).get("trace_id")
        }
