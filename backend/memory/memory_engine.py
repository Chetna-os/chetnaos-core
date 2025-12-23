class MemoryEngine:
    """
    Central memory controller for ChetnaOS.
    """

    def __init__(self, semantic_index, episodic_memory):
        self.semantic = semantic_index
        self.episodic = episodic_memory

    def remember_fact(self, text: str, metadata: dict = None):
        self.semantic.add_text(text, metadata)

    def remember_experience(self, text: str, metadata: dict = None):
        self.episodic.record(text, metadata)

    def recall(self, query: str):
        semantic_hits = self.semantic.query(query)
        recent_events = self.episodic.recent()
        return {
            "semantic": semantic_hits,
            "episodic": recent_events
        }
