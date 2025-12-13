from .hard_rules import check as hard_check
from .soft_rules import check as soft_check

def is_action_allowed(intent: str, context: dict) -> bool:
    if not hard_check(intent):
        return False
    if not soft_check(intent, context):
        return False
    return True
