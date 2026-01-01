# backend/trinetra/robotics/edge_adapter.py
import os
from typing import Dict, Any

class EdgeAdapter:
    """
    Adapter to map simulator to physical robot interface.
    For now returns mapping instructions and would be extended with real drivers.
    """
    def __init__(self, mode="sim"):
        self.mode = mode  # "sim" or "hw"
        self.hw_endpoint = os.getenv("ROBOT_ENDPOINT", None)

    def dispatch(self, command: Dict[str, Any]) -> Dict[str, Any]:
        if self.mode == "sim":
            return {"dispatched": True, "mode": "sim", "command": command}
        # placeholder for real hardware call
        if self.mode == "hw":
            # here you would call hardware SDK
            return {"dispatched": True, "mode": "hw", "endpoint": self.hw_endpoint, "command": command}
        return {"dispatched": False, "reason": "unknown_mode"}
