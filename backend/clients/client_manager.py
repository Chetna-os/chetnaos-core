# backend/clients/client_manager.py

from typing import Dict
from .client_loader import ClientLoader


class ClientManager:
    """
    Manages active clients and their configurations.
    """

    def _init_(self):
        self._clients: Dict[str, Dict] = {}

    def register_client(self, client_id: str):
        config = ClientLoader.load_client_config(client_id)
        self._clients[client_id] = config

    def get_client(self, client_id: str) -> Dict:
        if client_id not in self._clients:
            raise ValueError(f"Client not registered: {client_id}")
        return self._clients[client_id]

    def is_valid_client(self, client_id: str) -> bool:
        return client_id in self._clients

    def list_clients(self):
        return list(self._clients.keys())
