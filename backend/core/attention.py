# backend/core/attention.py

class AttentionEngine:
    def _init_(self):
        self.current_focus = None

    def set_focus(self, item: str, priority: int = 1):
        self.current_focus = {
            "item": item,
            "priority": priority
        }

    def get_focus(self):
        return self.current_focus

    def clear_focus(self):
        self.current_focus = None
