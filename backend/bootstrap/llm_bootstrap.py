"""
LLM Bootstrap
--------------
Initializes and registers the LLM provider at application startup.

This module provides explicit initialization of the LLM provider.
It does NOT auto-register on import - must be called explicitly.

Usage:
    from backend.bootstrap.llm_bootstrap import init_llm
    init_llm()  # Call once at application startup
"""

import os
import logging
from typing import Optional

from backend.integrations.llm import LLMRegistry
from backend.integrations.llm.groq_provider import GroqProvider

logger = logging.getLogger("ChetnaOS.bootstrap")


def init_llm() -> None:
    """
    Initialize and register the LLM provider.
    
    This function:
    1. Loads configuration from environment variables
    2. Instantiates GroqProvider with the configuration
    3. Registers it with LLMRegistry
    
    Environment variables:
        GROQ_API_KEY: Required. API key for Groq service
        DEFAULT_LLM_MODEL: Optional. Defaults to "llama3-8b-8192"
    
    Raises:
        ValueError: If GROQ_API_KEY is missing (raised by GroqProvider)
        RuntimeError: If registration fails for any other reason
    
    Note:
        This function should be called ONCE at application startup.
        It does NOT check if a provider is already registered.
    """
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("DEFAULT_LLM_MODEL", "llama3-8b-8192")
    
    # Build provider configuration
    # Note: GroqProvider will also check os.getenv("GROQ_API_KEY") as fallback
    # but we pass it explicitly for clarity
    config = {
        "api_key": api_key,
        "model": model,
    }
    
    try:
        # Instantiate provider (will raise ValueError if API key is missing)
        provider = GroqProvider(config)
        
        # Register with LLMRegistry (single source of truth)
        LLMRegistry.register(provider)
        
        logger.info(
            f"LLM provider registered: {provider.model}",
            extra={"model": provider.model, "provider": "groq"}
        )
        
    except ValueError as e:
        # API key missing or invalid configuration
        logger.warning(f"LLM Provider registration skipped: {e}")
        raise
    except Exception as e:
        # Unexpected error during registration
        logger.error(f"Failed to register LLM provider: {e}", exc_info=True)
        raise RuntimeError(f"LLM provider registration failed: {e}") from e

