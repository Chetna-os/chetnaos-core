# backend/billing/usage_tracker.py

from datetime import datetime
from typing import Dict


class UsageTracker:
    """
    Tracks per-client usage for billing & analytics.
    """

    def __init__(self):
        # client_id -> usage data
        self.usage_store: Dict[str, Dict] = {}

    def record_usage(
        self,
        client_id: str,
        *,
        messages: int = 0,
        tokens: int = 0,
        agent_calls: int = 0
    ):
        if client_id not in self.usage_store:
            self.usage_store[client_id] = {
                "messages": 0,
                "tokens": 0,
                "agent_calls": 0,
                "last_updated": None,
            }

        data = self.usage_store[client_id]
        data["messages"] += messages
        data["tokens"] += tokens
        data["agent_calls"] += agent_calls
        data["last_updated"] = datetime.utcnow().isoformat()

    def get_usage(self, client_id: str) -> Dict:
        return self.usage_store.get(client_id, {})

    def reset_usage(self, client_id: str):
        if client_id in self.usage_store:
            del self.usage_store[client_id]
