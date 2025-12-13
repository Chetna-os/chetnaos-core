class SalesWorkflow:
    def run(self, context: dict):
        if not context.get("qualified"):
            context["action"] = "nurture"
            return context

        score = context.get("lead_score", 0)

        if score >= 90:
            context["action"] = "close_now"
        elif score >= 70:
            context["action"] = "demo_call"
        else:
            context["action"] = "follow_up"

        return context
