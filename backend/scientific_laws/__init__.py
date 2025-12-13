"""
Scientific Laws Engine
----------------------
This package enforces physics, biology, and system-level constraints
on ChetnaOS decision-making, evolution, and autonomy.

No intelligence bypasses these laws.
"""

from .law_engine import ScientificLawEngine
from .energy_controller import EnergyController
from .entropy_guard import EntropyGuard
from .causality_checker import CausalityChecker
from .homeostasis_controller import HomeostasisController
from .evolution_pruner import EvolutionPruner

_all_ = [
    "ScientificLawEngine",
    "EnergyController",
    "EntropyGuard",
    "CausalityChecker",
    "HomeostasisController",
    "EvolutionPruner",
]
