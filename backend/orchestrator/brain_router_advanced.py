"""
ChetnaOS — BrainRouterAdvanced (AGI Orchestration Layer)

Purpose:
- High-level brain routing for AGI behavior
- Integrates intent, priority, dharma, workflows, reflection
- No conflict with existing agent router

Author: ChetnaOS Core
"""

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

    def _init_(self):
        self.intent_detector = IntentDetector()
        self.priority_engine = PriorityEngine()
        self.dharma_net = DharmaNet()
        self.reflection_engine = ReflectionEngine()

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

    def route(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
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

            response = {
                "status": "blocked",
                "reason": dharma_result["reason"],
                "trace_id": trace_id,
            }

            self._reflect(user_input, intent, response, context)
            return response

        # 4️⃣ Workflow Selection
        workflow = self._select_workflow(intent)
        logger.info(f"[{trace_id}] Selected workflow: {workflow._class.name_}")

        # 5️⃣ Execute Workflow
        output = workflow.execute(
            user_input=user_input,
            intent=intent,
            context=context
        )

        # 6️⃣ Reflection Loop
        self._reflect(user_input, intent, output, context)

        # 7️⃣ Metrics
        latency = time.time() - start_time
        record_metric("brain_router_latency", latency)

        logger.info(f"[{trace_id}] Routing completed in {latency:.2f}s")

        return {
            "status": "success",
            "intent": intent,
            "priority": priority,
            "output": output,
            "trace_id": trace_id,
        }

    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    def _select_workflow(self, intent: str):
        """
        Map intent to workflow.
        Default → custom flow
        """
        return self.workflows.get(intent, self.workflows["custom"])

    def _reflect(
        self,
        user_input: str,
        intent: str,
        output: Dict[str, Any],
        context: Dict[str, Any]
    ):
        """
        Feed experience back into reflection engine.
        """
        try:
            self.reflection_engine.record(
                user_input=user_input,
                intent=intent,
                output=output,
                context=context
            )
        except Exception as e:
            logger.error(f"Reflection failed: {e}")
