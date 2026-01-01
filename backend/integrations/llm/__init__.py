"""
LLM Integration Layer
---------------------
This module defines a unified interface for connecting
multiple Large Language Models (LLMs) with ChetnaOS.

Goals:
- Vendor agnostic design (OpenAI, Groq, Claude, Local)
- Safe switching of models without touching core logic
- Centralized control over cost, tokens, and behavior
- Future support for multi-model reasoning
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseLLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    Every LLM backend must implement this contract.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    @abstractmethod
    def generate(
        self,
        prompt: str,
        context: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response from LLM.

        Returns:
        {
            "text": str,
            "tokens_used": int,
            "model": str,
            "latency_ms": int
        }
        """
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> bool:
        """Check if LLM provider is reachable"""
        raise NotImplementedError


class LLMRegistry:
    """
    Registry to manage active LLM provider.
    Only one primary LLM is active at a time.
    """

    _active_provider: Optional[BaseLLMProvider] = None

    @classmethod
    def register(cls, provider: BaseLLMProvider) -> None:
        cls._active_provider = provider

    @classmethod
    def get(cls) -> BaseLLMProvider:
        if cls._active_provider is None:
            raise RuntimeError("No LLM provider registered")
        return cls._active_provider


class LLMResponseNormalizer:
    """
    Ensures all LLM outputs follow a consistent format
    before entering ChetnaOS reasoning layers.
    """

    @staticmethod
    def normalize(raw_response: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "text": raw_response.get("text", ""),
            "tokens_used": raw_response.get("tokens_used", 0),
            "model": raw_response.get("model", "unknown"),
            "latency_ms": raw_response.get("latency_ms", 0),
        }


__all__ = [
    "BaseLLMProvider",
    "LLMRegistry",
    "LLMResponseNormalizer",
]
