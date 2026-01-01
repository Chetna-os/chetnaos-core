# backend/scientific_laws/entropy_gaurd.py

class EntropyGuard:
    def __init__(self):
        self.max_entropy = 100.0  # abstract entropy units
        self.current_entropy = 0.0

    def allow(self, action: dict) -> bool:
        """Check if action maintains acceptable entropy levels"""
        entropy_cost = action.get("entropy_cost", 1.0)
        if self.current_entropy + entropy_cost > self.max_entropy:
            return False
        self.current_entropy += entropy_cost
        return True
