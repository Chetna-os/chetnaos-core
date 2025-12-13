class LeadWorkflow:
    def run(self, context: dict):
        lead = context.get("lead", {})
        score = 0

        if lead.get("budget"):
            score += 30
        if lead.get("urgency"):
            score += 40
        if lead.get("decision_maker"):
            score += 30

        context["lead_score"] = score
        context["qualified"] = score >= 60
        return context
