import os
from integrations.llm import LLMRegistry
from integrations.llm.groq_provider import GroqProvider


def bootstrap_llm():
    provider = os.getenv("ACTIVE_LLM_PROVIDER", "groq")

    if provider == "groq":
        LLMRegistry.register(GroqProvider())

    else:
        raise RuntimeError(f"Unsupported LLM provider: {provider}")