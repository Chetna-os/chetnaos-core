from typing import Dict, Any
import time


class RestCycle:
    """
    Periodic maintenance:
    - summarize
    - reset counters
    """

    def __init__(self, interval_sec: int = 300):
        self.interval_sec = interval_sec
        self._last_run = 0.0

    def due(self) -> bool:
        return (time.time() - self._last_run) >= self.interval_sec

    def run(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        self._last_run = time.time()
        # Minimal safe maintenance (no rewrite)
        summary = {"keys": list(memory.keys()), "size": len(memory)}
        return {"maintenance": "done", "summary": summary}
