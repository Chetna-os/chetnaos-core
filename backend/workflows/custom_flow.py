from integrations.llm import LLMRegistry
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

        # Try to get LLM, fallback to simple response if unavailable
        try:
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
        except RuntimeError as e:
            # LLM not registered, use fallback response
            response = {
                "text": f"I understand: {user_input}. How can I help you further?",
                "message": f"I understand: {user_input}. How can I help you further?"
            }
        except Exception as e:
            # Any other error, use safe fallback
            response = {
                "text": "I'm here to help. Could you please rephrase your request?",
                "message": "I'm here to help. Could you please rephrase your request?"
            }

        # 🔒 NORMALIZE + SANITIZE LLM OUTPUT (CRITICAL FIX)
        content = None

        if isinstance(response, dict):
            # Groq may return either `message` or `text`
            content = response.get("text") or response.get("message") or str(response)
        else:
            content = str(response)

        # Strip prompt echo and normalize
        if content:
            for marker in ["User Input:", "Detected Intent:", "Context:"]:
                if marker in content:
                    content = content.split(marker, 1)[0].strip()
            content = content.strip()

        # Ensure we always have a message
        if not content:
            content = "I understand your request. How can I help you further?"

        return {
            "workflow": self.name,
            "status": "completed",
            "output": {
                "message": content,
                "text": content,  # Alias for compatibility
                "reply": content   # Alias for easy extraction
            },
            "trace_id": context.get("trace_id")
        }