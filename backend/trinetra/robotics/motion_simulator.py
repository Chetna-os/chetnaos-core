# backend/trinetra/robotics/motion_simulator.py
from .virtual_actuator import VirtualActuator

class MotionSimulator:
    """
    High-level motion simulator that uses VirtualActuator.
    """
    def __init__(self):
        self.actuator = VirtualActuator()

    def execute(self, command: dict):
        # command validator could be extended
        return self.actuator.apply(command)
