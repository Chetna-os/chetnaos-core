import time
from typing import Dict, Any


class TemporalGuard:
    """
    Enforces temporal consistency:
    - cooldowns
    - last seen / last action
    """

    def __init__(self, cooldown_sec: int = 1):
        self.cooldown_sec = cooldown_sec
        self.state: Dict[str, float] = {}

    def allow(self, key: str) -> bool:
        now = time.time()
        last = self.state.get(key, 0.0)
        if now - last < self.cooldown_sec:
            return False
        self.state[key] = now
        return True

    def snapshot(self) -> Dict[str, Any]:
        return {"cooldown_sec": self.cooldown_sec, "state": dict(self.state)}
