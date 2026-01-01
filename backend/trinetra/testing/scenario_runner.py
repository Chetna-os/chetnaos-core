# backend/trinetra/testing/agent_testbench.py
import asyncio
import logging
from typing import Callable, Dict

LOG = logging.getLogger("trinetra.testbench")

class AgentTestbench:
    """
    Simple smoke tests for agents. Accepts an async or sync callable agent(text)->response.
    Returns simple metrics.
    """
    def __init__(self):
        self.smoke_samples = [
            "Hi, tell me about price.",
            "I want to book a visit.",
            "What is the location?",
            ""
        ]

    def _call_agent(self, agent: Callable, text: str):
        # support both async and sync
        res = agent(text)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res

    def run_smoke(self, agent: Callable) -> Dict:
        LOG.info("Running smoke tests")
        results = []
        for s in self.smoke_samples:
            try:
                r = self._call_agent(agent, s)
                ok = r is not None and len(str(r)) > 0
                results.append({"sample": s, "response": str(r)[:200], "ok": ok})
            except Exception as e:
                results.append({"sample": s, "error": str(e), "ok": False})
        passed = sum(1 for r in results if r.get("ok"))
        return {"total": len(results), "passed": passed, "results": results}
