# backend/clients/provisioning.py

import os
import json
from datetime import datetime


class ClientProvisioner:
    """
    Creates new client project structure.
    """

    BASE_PATH = "client_projects"

    @classmethod
    def provision_new_client(
        cls,
        client_id: str,
        *,
        name: str,
        plan: str = "basic"
    ):
        client_path = os.path.join(cls.BASE_PATH, client_id)

        if os.path.exists(client_path):
            raise FileExistsError(
                f"Client already exists: {client_id}"
            )

        os.makedirs(client_path, exist_ok=True)

        config = {
            "client_id": client_id,
            "name": name,
            "plan": plan,
            "created_at": datetime.utcnow().isoformat(),
            "features": {
                "agents": True,
                "memory": True,
                "billing": True,
                "self_learning": False
            }
        }

        with open(
            os.path.join(client_path, "config.json"),
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(config, f, indent=2)

        return config
