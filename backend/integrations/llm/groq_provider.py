import time
import os
from typing import Dict, Any, List, Optional

from backend.integrations.llm import BaseLLMProvider
from backend.integrations.llm.cost_gaurd import CostGuard


class GroqProvider(BaseLLMProvider):
    """
    Groq LLM Provider
    High-speed, low-cost inference backend
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.api_key = self.config.get("api_key") or os.getenv("GROQ_API_KEY")
        self.model = self.config.get("model", "llama3-70b-8192")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY missing")

        self.cost_guard = CostGuard(
            provider="groq",
            cost_per_1k_tokens=0.00059  # approx groq pricing
        )

    def generate(
        self,
        prompt: str,
        context: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ) -> Dict[str, Any]:

        start = time.time()

        # ---- Cost / Energy check before generation ----
        self.cost_guard.assert_allowed(prompt)

        # ---- MOCK CALL (replace with Groq SDK later) ----
        # This keeps backend runnable even without SDK
        response_text = f"[Groq:{self.model}] {prompt[:300]}"

        tokens_used = max(1, len(prompt) // 4)

        latency_ms = int((time.time() - start) * 1000)

        # ---- Register usage ----
        self.cost_guard.record_usage(tokens_used)

        return {
            "text": response_text,
            "tokens_used": tokens_used,
            "model": self.model,
            "latency_ms": latency_ms,
        }

    def health_check(self) -> bool:
        return True
