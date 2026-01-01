# backend/agents/base_agent.py
"""
Production-ready BaseAgent for ChetnaOS.
Provides:
 - structured logging
 - input validation
 - state (conversation memory)
 - metrics
 - process() wrapper to catch & return errors safely
"""

import logging
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger("chetna.agents")
if not logger.handlers:
    # simple console handler for development (replace in production)
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(h)
logger.setLevel(logging.INFO)


class AgentError(Exception):
    pass


class BaseAgent(ABC):
    def __init__(self, name: str = "BaseAgent", client_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.client_id = client_id
        self.config = config or {}
        self.state: Dict[str, Any] = {}                 # generic state storage
        self.metrics = {
            "total": 0,
            "success": 0,
            "fail": 0,
            "avg_response_time": 0.0
        }
        self._log = logger.getChild(self.name)
        self._log.info("Initialized", extra={"client_id": client_id})

    @abstractmethod
    async def handle(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Implement agent-specific behavior.
        Should return a dict with at minimum {"response": str}
        """
        raise NotImplementedError()

    async def process(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        start = datetime.utcnow()
        self.metrics["total"] += 1
        try:
            self._validate_input(text, context)
            self._log.debug("Processing request", extra={"text_len": len(text)})
            res = await self.handle(text, context or {})
            res_valid = self._normalize_response(res)
            self.metrics["success"] += 1
            elapsed = (datetime.utcnow() - start).total_seconds()
            self._update_avg_time(elapsed)
            self._log.info("Processed request", extra={"elapsed_s": elapsed})
            return res_valid
        except Exception as e:
            self.metrics["fail"] += 1
            self._log.exception("Error during process", exc_info=e)
            return {
                "success": False,
                "error": str(e),
                "fallback": self._fallback_response(),
                "agent": self.name
            }

    def _validate_input(self, text: Optional[str], context: Optional[Dict[str, Any]]):
        if not text or not isinstance(text, str):
            raise AgentError("Invalid text input")
        if context is not None and not isinstance(context, dict):
            raise AgentError("Context must be a dict")

    def _normalize_response(self, r: Any) -> Dict[str, Any]:
        if isinstance(r, str):
            return {"success": True, "response": r, "agent": self.name}
        if isinstance(r, dict):
            r.setdefault("success", True)
            r.setdefault("agent", self.name)
            return r
        raise AgentError("Invalid response type from agent")

    def _fallback_response(self) -> str:
        return "Kshama kijiye — mujhe abhi iska sahi jawaab nahi pata. Mai aapko connect kar dunga."

    def _update_avg_time(self, elapsed: float):
        total_success = max(1, self.metrics["success"])
        prev = self.metrics["avg_response_time"]
        self.metrics["avg_response_time"] = ((prev * (total_success - 1)) + elapsed) / total_success

    # state helpers
    def update_state(self, key: str, value: Any):
        self.state[key] = value
        self._log.debug("State updated", extra={"key": key})

    def get_state(self, key: str, default: Any = None):
        return self.state.get(key, default)

    def clear_state(self):
        self.state.clear()
        self._log.debug("State cleared")
