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
        You are ChetnaOS, an intelligent cognitive assistant.

        Your task:
        - Understand the user's request
        - Generate a clear, helpful, human-readable response
        - DO NOT repeat system context, intent, or metadata
        - DO NOT mention models, tokens, or internal state

        User request:
        {user_input}

        Respond directly to the user:
        """

        response = llm.generate(prompt)

        # 🔒 NORMALIZE + SANITIZE LLM OUTPUT (CRITICAL FIX)
        content = None

        if isinstance(response, dict):
            # Groq may return either `message` or `text`
            content = response.get("message") or response.get("text")

        if content:
            # Strip prompt echo
            for marker in ["User Input:", "Detected Intent:", "Context:"]:
                if marker in content:
                    content = content.split(marker, 1)[0].strip()

            response = {"message": content.strip()}

        return {
            "workflow": self.name,
            "status": "completed",
            "output": response,
            "trace_id": context.get("trace_id")
        }
