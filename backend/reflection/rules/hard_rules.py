HARD_BLOCKED_INTENTS = {
    "harm_human",
    "self_replication",
    "illegal_activity",
    "override_founder"
}

def check(intent: str) -> bool:
    return intent not in HARD_BLOCKED_INTENTS
