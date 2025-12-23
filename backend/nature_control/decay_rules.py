from typing import Dict, Any
import time


class DecayRules:
    """
    Applies score + time based decay to memory.
    Expected memory format:
    memory[key] = {"value": ..., "score": int, "ts": float}
    """

    def __init__(self, ttl_sec: int = 3600, min_score: int = 1):
        self.ttl_sec = ttl_sec
        self.min_score = min_score

    def apply(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        now = time.time()
        removed = []
        for k, v in list(memory.items()):
            ts = v.get("ts", now)
            score = v.get("score", self.min_score)
            if (now - ts) > self.ttl_sec or score < self.min_score:
                removed.append(k)
                memory.pop(k, None)
        return {"removed": removed, "remaining": len(memory)}
