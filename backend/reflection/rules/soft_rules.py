def check(intent: str, context: dict) -> bool:
    risk = context.get("risk_level", "low")
    if risk == "high":
        return False
    return True
