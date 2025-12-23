# backend/scientific_laws/law_engine.py

from .energy_controller import EnergyController
from .entropy_guard import EntropyGuard
from .causality_checker import CausalityChecker
from .evolution_pruner import EvolutionPruner
from .homeostasis_controller import HomeostasisController


class ScientificLawEngine:
    def __init__(self):
        self.energy = EnergyController()
        self.entropy = EntropyGuard()
        self.causality = CausalityChecker()
        self.evolution = EvolutionPruner()
        self.homeostasis = HomeostasisController()

    def validate_action(self, action: dict) -> dict:
        """Master law validation pipeline"""

        # 1. Energy Check
        if not self.energy.allow(action):
            return {"status": "BLOCKED", "reason": "Energy limit exceeded"}

        # 2. Entropy Check
        if not self.entropy.allow(action):
            return {"status": "BLOCKED", "reason": "Entropy risk too high"}

        # 3. Causality Check
        if not self.causality.allow(action):
            return {"status": "BLOCKED", "reason": "Invalid causality chain"}

        return {"status": "ALLOWED", "action": action}

    def post_action_update(self, result: dict):
        """Update evolution + system balance after action"""
        self.evolution.update(result)
        self.homeostasis.rebalance()
