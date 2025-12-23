class SpeakAdapter:
    """
  Converts internal AGI output into user-visible response
  """

    @staticmethod
    def format(response: dict) -> dict:
        if not response:
            return {"text": "No response generated."}

        if response.get("status") == "blocked":
            return {
                "text":
                f"⚠️ Request blocked due to Dharma rule: {response.get('reason')}"
            }

        output = response.get("output", {})

        if isinstance(output, dict):
            return {"text": output.get("message", str(output))}

        return {"text": str(output)}
