"""
ChetnaOS — BrainRouterAdvanced (AGI Orchestration Layer)

Purpose:
- High-level brain routing for AGI behavior
- Integrates intent, priority, dharma, workflows, reflection
- No conflict with existing agent router

Author: ChetnaOS Core
"""
from core.decision_states import DecisionState
from nature_control import TemporalGuard, SilenceEngine, RestCycle, DecayRules, Limits
from adapters.speak_adapter import SpeakAdapter
from typing import Dict, Any, Optional
import uuid
import time
import logging

# --- Core imports ---
from orchestrator.intent_detector import IntentDetector
from orchestrator.priority_engine import PriorityEngine

# --- Reflection & Dharma ---
from reflection.dharma_net import DharmaNet
from reflection.reflection_engine import ReflectionEngine

# --- Workflows ---
from workflows.custom_flow import CustomFlow
from workflows.sales_flow import SalesFlow
from workflows.lead_flow import LeadFlow

# --- Monitoring ---
from monitoring.metrics import record_metric

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
        try:
            from core.founder_queue import FounderQueue
            self.founder_queue = FounderQueue()
        except ImportError:
            self.founder_queue = None
            logger.warning("FounderQueue not found, proceeding without it")

        self.wisdom_layer = None
        try:
            # Check if wisdom directory exists
            import os
            if os.path.exists("wisdom"):
                from wisdom.wisdom_layer import WisdomLayer
                self.wisdom_layer = WisdomLayer()
        except ImportError:
            logger.warning("WisdomLayer not found, proceeding with defaults")

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
        decision = DecisionState.ALLOW.value
        wisdom_output = {"verdict": decision, "reason": "Default bypass"}

        if self.wisdom_layer:
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

        if decision == DecisionState.REQUIRE_FOUNDER.value and self.founder_queue:
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

        # 5️⃣ Workflow Selection
        workflow = self._select_workflow(intent)
        logger.info(f"[{trace_id}] Selected workflow: {workflow.__class__.__name__}")

        # 6️⃣ Execute Workflow
        output = workflow.execute(
            user_input=user_input,
            intent=intent,
            context=context
        )

        # 7️⃣ Reflection Loop
        self._reflect(user_input, intent, output, context)

        # 8️⃣ Metrics
        latency = time.time() - start_time
        record_metric("brain_router_latency", latency)

        logger.info(f"[{trace_id}] Routing completed in {latency:.2f}s")

        # Normalize workflow output to extract reply text
        reply_text = None
        if isinstance(output, dict):
            # Check nested output structure
            nested_output = output.get("output")
            if isinstance(nested_output, dict):
                reply_text = nested_output.get("message") or nested_output.get("text") or nested_output.get("reply")
            elif isinstance(nested_output, str):
                reply_text = nested_output
            # Check direct fields
            if not reply_text:
                reply_text = output.get("message") or output.get("text") or output.get("reply")
        elif isinstance(output, str):
            reply_text = output

        # Fallback if no reply found
        if not reply_text:
            reply_text = "Request processed successfully"

        return {
            "status": "success",
            "trace_id": trace_id,
            "output": {
                "message": reply_text,
                "intent": intent,
                "workflow": workflow.__class__.__name__
            },
            "reply": reply_text  # Add direct reply field for easy extraction
        }

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

brain_router = BrainRouterAdvanced()
