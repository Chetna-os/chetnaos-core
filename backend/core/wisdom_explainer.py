# backend/core/wisdom_explainer.py

from typing import Dict, Any, List
from datetime import datetime
import uuid


def explain_decision(*,
                     raw_input: str,
                     detected_intent: str,
                     intent_confidence: float,
                     user_type: str,
                     risk_level: str,
                     sensitivity: List[str],
                     verdict: str,
                     reason: str,
                     verdict_confidence: float,
                     constraints_triggered: List[Dict[str, str]],
                     values_consulted: List[Dict[str, str]],
                     memory_considered: Dict[str, Any],
                     final_status: str,
                     next_step: str | None = None) -> Dict[str, Any]:
    """
    Canonical Wisdom Explainability Output.
    THIS IS THE SINGLE SOURCE OF TRUTH.
    """

    return {
        "trace_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "input": {
            "raw_text": raw_input,
            "detected_intent": detected_intent,
            "confidence": round(intent_confidence, 2)
        },
        "context": {
            "user_type": user_type,
            "risk_level": risk_level,
            "sensitivity": sensitivity
        },
        "wisdom_evaluation": {
            "verdict": verdict,
            "reason": reason,
            "confidence": round(verdict_confidence, 2)
        },
        "constraints_triggered": constraints_triggered,
        "values_consulted": values_consulted,
        "memory_considered": {
            "episodic": memory_considered.get("episodic", False),
            "semantic": memory_considered.get("semantic", False),
            "note": memory_considered.get("note")
        },
        "final_action": {
            "status": final_status,
            "next_step": next_step
        }
    }
