"""
Local LLM Provider (Placeholder)
--------------------------------
This is a placeholder for local LLM integration (e.g., Ollama, llama.cpp).
Implement BaseLLMProvider interface when needed.
"""

from integrations.llm import BaseLLMProvider
from typing import Dict, Any, List, Optional


class LocalLLMProvider(BaseLLMProvider):
    """Local LLM Provider - Not yet implemented"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        raise NotImplementedError("LocalLLMProvider is not yet implemented")
    
    def generate(self, prompt: str, context: Optional[List[Dict[str, str]]] = None, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("LocalLLMProvider is not yet implemented")
    
    def health_check(self) -> bool:
        return False
