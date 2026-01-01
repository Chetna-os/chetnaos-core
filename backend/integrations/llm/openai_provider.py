"""
OpenAI LLM Provider (Placeholder)
----------------------------------
This is a placeholder for OpenAI integration.
Implement BaseLLMProvider interface when needed.
"""

from backend.integrations.llm import BaseLLMProvider
from typing import Dict, Any, List, Optional


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM Provider - Not yet implemented"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        raise NotImplementedError("OpenAIProvider is not yet implemented")
    
    def generate(self, prompt: str, context: Optional[List[Dict[str, str]]] = None, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("OpenAIProvider is not yet implemented")
    
    def health_check(self) -> bool:
        return False
