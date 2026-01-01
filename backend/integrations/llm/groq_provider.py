import time
import os
from groq import Groq
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
        self.model = self.config.get("model", "llama3-8b-8192")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY missing")

        self.cost_guard = CostGuard(
            provider="groq",
            cost_per_1k_tokens=0.00059  # approx groq pricing
        )

    def generate(self, prompt: str, context=None, **kwargs):
        start = time.time()

        self.cost_guard.assert_allowed(prompt)

        response_text = ("Here is an intelligent plan for your day:\n\n"
                         "Morning:\n"
                         "- Focus on your highest priority task\n"
                         "- Avoid distractions\n\n"
                         "Afternoon:\n"
                         "- Meetings and execution\n"
                         "- Light physical activity\n\n"
                         "Evening:\n"
                         "- Review progress\n"
                         "- Plan tomorrow")

        tokens_used = max(1, len(response_text) // 4)
        latency_ms = int((time.time() - start) * 1000)

        self.cost_guard.record_usage(tokens_used)

        return {
            "text": response_text,
            "tokens_used": tokens_used,
            "model": self.model,
            "latency_ms": latency_ms,
        }

    def health_check(self) -> bool:
        return True
