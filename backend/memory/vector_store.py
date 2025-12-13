import math


class VectorStore:
    """
    Simple in-memory vector store.
    Can be replaced later with FAISS / Milvus / Pinecone.
    """

    def _init_(self):
        self.vectors = []  # [(id, vector, metadata)]

    def add(self, item_id: str, vector: list[float], metadata: dict = None):
        self.vectors.append((item_id, vector, metadata or {}))

    def _cosine_similarity(self, v1, v2):
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        return dot / (norm1 * norm2 + 1e-8)

    def search(self, query_vector: list[float], top_k: int = 3):
        scored = []
        for item_id, vector, metadata in self.vectors:
            score = self._cosine_similarity(query_vector, vector)
            scored.append((score, item_id, metadata))
        scored.sort(reverse=True)
        return scored[:top_k]
