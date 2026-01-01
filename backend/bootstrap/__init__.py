"""
Bootstrap Layer
----------------
Initialization code that runs ONCE at application startup.
This layer handles:
- LLM provider registration
- System-wide component initialization
- Environment configuration

Rules:
- NO auto-registration on import
- NO circular dependencies
- Explicit initialization only
"""

