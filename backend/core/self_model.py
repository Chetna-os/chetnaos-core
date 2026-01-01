# backend/core/self_model.py

class SelfModel:
    def __init__(self):
        self.identity = {
            "name": "Chetna",
            "version": "v1",
            "role": "Assisted AGI Core"
        }

        self.state = {
            "energy": 100,
            "stability": 1.0,
            "learning_enabled": False
        }

    def get_identity(self):
        return self.identity

    def update_state(self, key: str, value):
        self.state[key] = value

    def get_state(self):
        return self.state
