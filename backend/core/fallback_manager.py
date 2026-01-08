"""
Fallback Manager
----------------
Central authority for degradation, pause, and human handoff.
No module is allowed to bypass this.
"""

import os
import json
from datetime import datetime
from typing import Dict

from config.fallback_config import FALLBACK_CONFIG


class FallbackManager:
    """
    Central fallback decision engine.
    Decides system behavior under uncertainty, cost, time, or dharma violations.
    """

    def __init__(self):
        self.log_file = "backend/logs/fallback_events.json"

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def evaluate(self,
                 uncertainty: float = 0.0,
                 cost: float = 0.0,
                 runtime: float = 0.0,
                 dharma_violation: bool = False) -> Dict:
        """
        Evaluate system state and decide fallback level.

        Returns:
            dict with fallback_level, action, reason
        """

        level = self._decide_level(uncertainty=uncertainty,
                                   cost=cost,
                                   runtime=runtime,
                                   dharma_violation=dharma_violation)

        decision = {
            "timestamp": datetime.utcnow().isoformat(),
            "fallback_level": level,
            "action": FALLBACK_CONFIG["levels"][level],
            "signals": {
                "uncertainty": uncertainty,
                "cost": cost,
                "runtime": runtime,
                "dharma_violation": dharma_violation
            }
        }

        self._log_event(decision)
        return decision

    # --------------------------------------------------
    # Internal Logic
    # --------------------------------------------------

    def _decide_level(self, uncertainty: float, cost: float, runtime: float,
                      dharma_violation: bool) -> int:
        """
        Decide fallback level based on signals.
        Higher number = deeper fallback.
        """

        if dharma_violation:
            return 4  # HARD_STOP

        if uncertainty >= FALLBACK_CONFIG["max_uncertainty"]:
            return 3  # REFLECTION

        if cost >= FALLBACK_CONFIG["max_cost_per_task"]:
            return 2  # HUMAN_HANDOFF

        if runtime >= FALLBACK_CONFIG["max_time_sec"]:
            return 1  # DEGRADE

        return FALLBACK_CONFIG["default_level"]

    # --------------------------------------------------
    # Logging (Self-Healing)
    # --------------------------------------------------

    def _log_event(self, event: Dict):
        """
        Append fallback decision to audit log.
        Creates directories automatically if missing.
        Preserves existing metadata structure with events array.
        """

        try:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

            data = None
            if os.path.exists(self.log_file):
                try:
                    with open(self.log_file, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:
                            data = json.loads(content)
                except (json.JSONDecodeError, IOError):
                    data = None

            if data is None or not isinstance(data, dict):
                data = {
                    "meta": {
                        "purpose": "Authoritative log of fallback decisions",
                        "authority": "fallback_manager",
                        "write_policy": "append_only",
                        "decision_override": "not_allowed",
                        "version": "v0.1"
                    },
                    "events": []
                }

            if "events" not in data or not isinstance(data["events"], list):
                data["events"] = []

            data["events"].append(event)

            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print("[FallbackManager] Logging failed:", e)
