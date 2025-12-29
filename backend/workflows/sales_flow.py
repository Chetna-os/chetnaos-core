from typing import Dict, Any
from backend.integrations.llm import LLMRegistry


class SalesFlow:
    """
    Sales-specific workflow.
    """

    def execute(self, user_input: str, intent: str,
                context: Dict[str, Any]) -> Dict[str, Any]:
        llm = LLMRegistry.get()

        prompt = f"""
        You are a sales assistant.

        User Input:
        {user_input}

        Context:
        {context}
        """

        response = llm.generate(prompt)

        return {
            "workflow": "sales",
            "status": "completed",
            "output": response,
            "trace_id": context.get("wisdom", {}).get("trace_id")
        }
