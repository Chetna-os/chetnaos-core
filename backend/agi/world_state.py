# backend/agi/world_state.py

from typing import Dict, Any
from datetime import datetime


class WorldState:
    """
    Tracks real-world state of the system.
    This is the 'Reality Anchor' for AGI.
    """

    def _init_(self):
        self.state: Dict[str, Any] = {
            "clients": {},
            "leads": [],
            "tasks": [],
            "income": 0,
            "expenses": 0,
            "last_updated": datetime.utcnow().isoformat()
        }

    def update(self, key: str, value: Any):
        self.state[key] = value
        self.state["last_updated"] = datetime.utcnow().isoformat()

    def add_lead(self, lead: Dict[str, Any]):
        self.state["leads"].append(lead)
        self.state["last_updated"] = datetime.utcnow().isoformat()

    def add_task(self, task: Dict[str, Any]):
        self.state["tasks"].append(task)
        self.state["last_updated"] = datetime.utcnow().isoformat()

    def record_income(self, amount: float):
        self.state["income"] += amount
        self.state["last_updated"] = datetime.utcnow().isoformat()

    def record_expense(self, amount: float):
        self.state["expenses"] += amount
        self.state["last_updated"] = datetime.utcnow().isoformat()

    def snapshot(self) -> Dict[str, Any]:
        return dict(self.state)
