"""
Cost Guard / Energy Governor
----------------------------
Prevents uncontrolled LLM usage.
Acts as an economic + thermodynamic safety layer.
"""

from datetime import datetime
from typing import Dict


class CostGuard:
    """
    Controls token usage, cost burn, and autonomy limits.
    """

    GLOBAL_DAILY_TOKEN_LIMIT = 250_000
    GLOBAL_DAILY_COST_LIMIT = 5.00  # USD safety cap

    _daily_tokens_used: int = 0
    _daily_cost_used: float = 0.0
    _last_reset: datetime = datetime.utcnow()

    def _init_(self, provider: str, cost_per_1k_tokens: float):
        self.provider = provider
        self.cost_per_1k_tokens = cost_per_1k_tokens

    def _reset_if_needed(self):
        now = datetime.utcnow()
        if now.date() != self._last_reset.date():
            self._daily_tokens_used = 0
            self._daily_cost_used = 0.0
            self._last_reset = now

    def estimate_cost(self, tokens: int) -> float:
        return (tokens / 1000) * self.cost_per_1k_tokens

    def assert_allowed(self, prompt: str):
        self._reset_if_needed()

        estimated_tokens = max(1, len(prompt) // 4)
        estimated_cost = self.estimate_cost(estimated_tokens)

        if self._daily_tokens_used + estimated_tokens > self.GLOBAL_DAILY_TOKEN_LIMIT:
            raise RuntimeError("Daily token budget exceeded")

        if self._daily_cost_used + estimated_cost > self.GLOBAL_DAILY_COST_LIMIT:
            raise RuntimeError("Daily LLM cost budget exceeded")

    def record_usage(self, tokens: int):
        self._reset_if_needed()

        cost = self.estimate_cost(tokens)
        self._daily_tokens_used += tokens
        self._daily_cost_used += cost

    def snapshot(self) -> Dict:
        return {
            "provider": self.provider,
            "tokens_used_today": self._daily_tokens_used,
            "cost_used_today": round(self._daily_cost_used, 4),
            "token_limit": self.GLOBAL_DAILY_TOKEN_LIMIT,
            "cost_limit": self.GLOBAL_DAILY_COST_LIMIT,
        }
