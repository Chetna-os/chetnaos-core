# backend/clients/isolation.py

from typing import Dict


class ClientIsolation:
    """
    Ensures strict isolation between client data.
    """

    def __init__(self):
        self._memory_store: Dict[str, Dict] = {}

    def get_client_memory(self, client_id: str) -> Dict:
        if client_id not in self._memory_store:
            self._memory_store[client_id] = {}
        return self._memory_store[client_id]

    def clear_client_memory(self, client_id: str):
        if client_id in self._memory_store:
            del self._memory_store[client_id]
