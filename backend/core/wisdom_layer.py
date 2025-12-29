"""
Buddhi Gate — Active Decision Layer
----------------------------------
Role:
- Final moral / strategic / safety evaluator
- Consults beliefs, constraints, smriti
- Enforces Founder-in-Loop when required

This is NOT memory.
This is NOT routing.
This is judgment.
"""

from enum import Enum
from typing import Dict, Any, Optional
import uuid
import logging

logger = logging.getLogger("ChetnaOS.Buddhi")


# ================================
# Decision States (LOCK THIS)
# ================================
from backend.core.decision_states import DecisionState
    ALLOW = "allow"
    ALLOW_WITH_WARNING = "allow_with_warning"
    DEFER = "defer"
    REQUIRE_FOUNDER = "require_founder"
    REJECT = "reject"
    SAFE_MODE = "safe_mode"


# ================================
# Buddhi Gate
# ================================
class BuddhiGate:
    """
    Active evaluator.
    Knows when NOT to act.
    """

    def __init__(self,
                 value_store,
                 constraint_memory,
                 memory_policy=None,
                 founder_required_actions: Optional[list] = None):
        self.value_store = value_store
        self.constraint_memory = constraint_memory
        self.memory_policy = memory_policy
        self.founder_required_actions = founder_required_actions or []

    # --------------------------------
    # Core Evaluation Entry Point
    # --------------------------------
    def evaluate(self,
                 proposed_action: str,
                 intent: str,
                 context: Dict[str, Any],
                 smriti: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Returns:
        {
            verdict: BuddhiVerdict,
            reason: str,
            trace_id: str
        }
        """

        trace_id = str(uuid.uuid4())

        # 1️⃣ Hard constraints (NO negotiation)
        violated = self.constraint_memory.check_violation(
            proposed_action=proposed_action, context=context)

        if violated:
            logger.warning(f"[BUDDHI] Constraint violated: {violated}")
            return self._decision(BuddhiVerdict.REJECT,
                                  f"Constraint violated: {violated}", trace_id)

        # 2️⃣ Founder-in-loop mandatory actions
        if proposed_action in self.founder_required_actions:
            logger.info("[BUDDHI] Founder approval required")
            return self._decision(BuddhiVerdict.REQUIRE_FOUNDER,
                                  "Founder approval required for this action",
                                  trace_id)

        # 3️⃣ Value alignment check
        alignment = self.value_store.evaluate_alignment(action=proposed_action,
                                                        intent=intent,
                                                        context=context)

        if not alignment.get("aligned", True):
            severity = alignment.get("severity", "medium")

            if severity == "high":
                return self._decision(
                    BuddhiVerdict.REJECT,
                    alignment.get("reason", "Value misalignment"), trace_id)

            return self._decision(
                BuddhiVerdict.ALLOW_WITH_WARNING,
                alignment.get("reason", "Partial value misalignment"),
                trace_id)

        # 4️⃣ Smriti-based risk signal (optional, non-blocking Phase-1)
        if smriti:
            risk = smriti.get("risk_signal")
            if risk == "high":
                return self._decision(
                    BuddhiVerdict.DEFER,
                    "Historical risk detected — defer execution", trace_id)

        # 5️⃣ Default allow
        return self._decision(DecisionState.ALLOW, "Action approved by Buddhi",
                              trace_id)

    # --------------------------------
    # Internal helper
    # --------------------------------
    def _decision(self, verdict: BuddhiVerdict, reason: str, trace_id: str):
        return {
            "verdict": verdict.value,
            "reason": reason,
            "trace_id": trace_id
        }
