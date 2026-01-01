# backend/core/chetna_core.py

from .attention import AttentionEngine
from .reasoning import ReasoningEngine
from .self_model import SelfModel


class ChetnaCore:
    def __init__(self):
        self.attention = AttentionEngine()
        self.reasoning = ReasoningEngine()
        self.self_model = SelfModel()

    def think(self, context: dict, goal: str):
        # Step 1: Focus
        self.attention.set_focus(goal, priority=1)

        # Step 2: Reason
        decision = self.reasoning.reason(context, goal)

        # Step 3: Update internal state (safe)
        self.self_model.update_state("energy", self.self_model.state["energy"] - 1)

        return {
            "focus": self.attention.get_focus(),
            "decision": decision,
            "self_state": self.self_model.get_state()
        }
