from .vector_store import VectorStore


class SemanticIndex:
    """
    Semantic memory for meanings, concepts, facts.
    """

    def __init__(self, embedder):
        self.embedder = embedder
        self.store = VectorStore()

    def add_text(self, text: str, metadata: dict = None):
        vector = self.embedder(text)
        self.store.add(text, vector, metadata)

    def query(self, text: str, top_k: int = 3):
        query_vector = self.embedder(text)
        return self.store.search(query_vector, top_k)
