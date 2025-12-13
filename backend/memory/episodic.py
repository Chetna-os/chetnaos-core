import time


class EpisodicMemory:
    """
    Stores time-stamped experiences.
    """

    def _init_(self):
        self.events = []

    def record(self, content: str, metadata: dict = None):
        self.events.append({
            "time": time.time(),
            "content": content,
            "metadata": metadata or {}
        })

    def recent(self, limit: int = 5):
        return self.events[-limit:]
