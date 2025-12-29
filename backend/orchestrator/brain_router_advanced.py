"""
ChetnaOS — BrainRouterAdvanced (AGI Orchestration Layer)

Purpose:
- High-level brain routing for AGI behavior
- Integrates intent, priority, dharma, workflows, reflection
- No conflict with existing agent router

Author: ChetnaOS Core
"""
from backend.core.decision_states import DecisionState
from backend.nature_control import TemporalGuard, SilenceEngine, RestCycle, DecayRules, Limits
from backend.adapters.speak_adapter import SpeakAdapter
from typing import Dict, Any, Optional
import uuid
import time
import logging

# --- Core imports ---
from backend.orchestrator.intent_detector import IntentDetector
from backend.orchestrator.priority_engine import PriorityEngine

# --- Reflection & Dharma ---
from backend.reflection.dharma_net import DharmaNet
from backend.reflection.reflection_engine import ReflectionEngine

# --- Workflows ---
from backend.workflows.custom_flow import CustomFlow
from backend.workflows.sales_flow import SalesFlow
from backend.workflows.lead_flow import LeadFlow

# --- Monitoring ---
from backend.monitoring.metrics import record_metric

logger = logging.getLogger("BrainRouterAdvanced")
logger.setLevel(logging.INFO)


class BrainRouterAdvanced:
    """
    AGI Brain Router v2
    -------------------
    Central decision brain of ChetnaOS.

    Flow:
    Input → Intent → Priority → Dharma → Workflow → Reflection → Output
    """

    def __init__(self):
        from backend.core.founder_queue import FounderQueue
        self.founder_queue = FounderQueue()
        self.intent_detector = IntentDetector()
        self.priority_engine = PriorityEngine()
        self.dharma_net = DharmaNet()
        self.reflection_engine = ReflectionEngine()
        self.temporal = TemporalGuard(cooldown_sec=1)
        self.silence = SilenceEngine(min_confidence=0.35)
        self.rest = RestCycle(interval_sec=300)
        self.decay = DecayRules(ttl_sec=3600, min_score=1)
        self.limits = Limits(max_autonomy_sec=10, max_tokens=1200)

        # Workflow registry (extensible)
        self.workflows = {
            "sales": SalesFlow(),
            "lead": LeadFlow(),
            "custom": CustomFlow(),
        }

        logger.info("🧠 BrainRouterAdvanced initialized")

    # ------------------------------------------------------------------
    # Public Entry Point
    # ------------------------------------------------------------------

    def route(self,
              user_input: str,
              context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main AGI routing entry.

        Args:
            user_input: Raw user input
            context: Optional runtime context

        Returns:
            Structured AGI response
        """
        start_time = time.time()
        trace_id = str(uuid.uuid4())

        context = context or {}
        context["trace_id"] = trace_id

        logger.info(f"[{trace_id}] Incoming input received")

        # 1️⃣ Intent Detection
        intent = self.intent_detector.detect(user_input)
        logger.info(f"[{trace_id}] Detected intent: {intent}")

        # 2️⃣ Priority Scoring
        priority = self.priority_engine.score(intent, context)
        logger.info(f"[{trace_id}] Priority score: {priority}")

        # 3️⃣ Dharma Validation
        dharma_result = self.dharma_net.validate(
            intent=intent,
            priority=priority,
            context=context
        )

        if not dharma_result["allowed"]:
            logger.warning(f"[{trace_id}] Dharma violation detected")

            return {
                "status": "blocked",
                "reason": dharma_result["reason"],
                "trace_id": trace_id,
            }

        # 4️⃣ Wisdom Layer (Buddhi / Wisdom Gate)
        wisdom_output = self.wisdom_layer.evaluate(
            intent=intent,
            context=context,
            priority=priority,
            trace_id=trace_id
        )

        decision = wisdom_output.get("verdict")

        if decision == DecisionState.REJECT.value:
            return {
                "status": "blocked",
                "reason": wisdom_output.get("reason"),
                "trace_id": trace_id
            }

        self.founder_queue.add(trace_id, {
            "user_input": user_input,
            "intent": intent,
            "priority": priority,
            "context": context,
            "wisdom": wisdom_output
        })

        return {
            "status": "pending_approval",
            "reason": wisdom_output.get("reason"),
            "trace_id": trace_id
        }

        if decision == DecisionState.DEFER.value:
            return {
                "status": "deferred",
                "reason": wisdom_output.get("reason"),
                "trace_id": trace_id
            }

        # ALLOW / ALLOW_WITH_WARNING
        context["wisdom"] = wisdom_output

            self._reflect(user_input, intent, response, context)
            return response

        
    # Internal Helpers

    def _select_workflow(self, intent: str):
        """
        Map intent to workflow.
        Default → custom flow
        """
        return self.workflows.get(intent, self.workflows["custom"])

    def _reflect(self, user_input: str, intent: str, output: Dict[str, Any],
                 context: Dict[str, Any]):
        """
        Feed experience back into reflection engine.
        """
        try:
            self.reflection_engine.record(user_input=user_input,
                                          intent=intent,
                                          output=output,
                                          context=context)
        except Exception as e:
            logger.error(f"Reflection failed: {e}")
