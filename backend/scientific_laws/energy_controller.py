# backend/scientific_laws/energy_controller.py

class EnergyController:
    def __init__(self):
        self.daily_budget = 100.0   # abstract energy units
        self.used = 0.0

    def allow(self, action: dict) -> bool:
        cost = action.get("energy_cost", 1.0)
        if self.used + cost > self.daily_budget:
            return False
        self.used += cost
        return True
