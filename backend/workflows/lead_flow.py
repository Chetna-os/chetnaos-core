from typing import Dict, Any


class LeadFlow:
    """
    Lead qualification workflow handler.
    """

    def execute(
        self,
        user_input: str,
        intent: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the lead qualification workflow.
        """
        lead = context.get("lead", {})
        score = 0

        if lead.get("budget"):
            score += 30
        if lead.get("urgency"):
            score += 40
        if lead.get("decision_maker"):
            score += 30

        return {
            "workflow": "lead",
            "lead_score": score,
            "qualified": score >= 60,
            "message": f"Lead flow executed for: {user_input}",
            "intent": intent
        }
