from typing import Dict, Any
import time


class FounderQueue:
    """
    Stores pending founder-approval decisions
    """

    def __init__(self):
        self._queue: Dict[str, Dict[str, Any]] = {}

    def add(self, trace_id: str, payload: Dict[str, Any]):
        self._queue[trace_id] = {
            "payload": payload,
            "timestamp": time.time(),
            "status": "pending"
        }

    def get(self, trace_id: str):
        return self._queue.get(trace_id)

    def approve(self, trace_id: str):
        if trace_id in self._queue:
            self._queue[trace_id]["status"] = "approved"
            return self._queue[trace_id]
        return None

    def reject(self, trace_id: str):
        if trace_id in self._queue:
            self._queue[trace_id]["status"] = "rejected"
            return self._queue[trace_id]
        return None
