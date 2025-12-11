# backend/trinetra/robotics/virtual_actuator.py
from typing import Dict, Any

class VirtualActuator:
    """
    Minimal virtual actuator interface - returns ack + simulated state.
    """
    def _init_(self):
        self.state = {"position": [0,0,0], "holding": None}

    def apply(self, command: Dict[str, Any]) -> Dict[str, Any]:
        # support simple cmds: move / pick / place
        if "move" in command:
            # naive movement: increment x by steps if numeric
            steps = command.get("steps", 1)
            self.state["position"][0] += steps
            return {"ok": True, "state": self.state.copy(), "action": f"moved {steps}"}
        if "pick" in command:
            item = command.get("pick")
            self.state["holding"] = item
            return {"ok": True, "state": self.state.copy(), "action": f"picked {item}"}
        return {"ok": False, "reason": "unknown_command"}
