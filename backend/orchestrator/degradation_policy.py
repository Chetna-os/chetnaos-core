class DegradationPolicy:
    """
  Controls how system degrades when fallback is triggered.
  """

    def apply(self, level: int) -> dict:
        if level == 0:
            return {
                "action": "STOP",
                "message": "System halted due to critical boundary breach."
            }

        if level == 1:
            return {
                "mode": "SAFE_MODE",
                "llm_temperature": 0.2,
                "creativity": False,
                "self_evolution": False
            }

        if level == 2:
            return {
                "mode": "HUMAN_REQUIRED",
                "message": "Human guidance required to proceed."
            }

        if level == 3:
            return {
                "mode": "REFLECTION_ONLY",
                "learning": False,
                "action": "LOG_AND_WAIT"
            }

        return {"mode": "RECOVERY", "constraints": "LIMITED"}
