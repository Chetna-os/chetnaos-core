# backend/clients/client_loader.py

import json
import os
from typing import Dict


class ClientLoader:
    """
    Loads client configuration from client_projects folder.
    """

    BASE_PATH = "client_projects"

    @classmethod
    def load_client_config(cls, client_id: str) -> Dict:
        config_path = os.path.join(
            cls.BASE_PATH,
            client_id,
            "config.json"
        )

        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Config not found for client: {client_id}"
            )

        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
