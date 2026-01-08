from typing import Dict, Any
from integrations.llm import LLMRegistry


class LeadFlow:
    """
    Lead qualification workflow.
    Executes ONLY if BrainRouter allows.
    """

    def execute(self, user_input: str, intent: str,
                context: Dict[str, Any]) -> Dict[str, Any]:
        llm = LLMRegistry.get()

        prompt = f"""
        You are a lead qualification agent.

        User Input:
        {user_input}

        Context:
        {context}
        """

        response = llm.generate(prompt)

        return {
            "workflow": "lead",
            "status": "completed",
            "output": response,
            "trace_id": context.get("wisdom", {}).get("trace_id")
        }
