def requires_human_review(context: dict) -> bool:
    return context.get("critical", False)
