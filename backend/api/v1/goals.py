from fastapi import APIRouter, HTTPException
from clients.client_manager import ClientManager

router = APIRouter(prefix="/client", tags=["Client Management"])

client_manager = ClientManager()

@router.post("/register")
async def register_client(payload: dict):
    """
    Register a new client with config.
    """
    name = payload.get("name")
    config = payload.get("config", {})

    if not name:
        raise HTTPException(400, "Client name is required")

    client_id = client_manager.create_client(name, config)

    return {
        "success": True,
        "client_id": client_id
    }


@router.get("/{client_id}")
async def get_client_config(client_id: str):
    config = client_manager.load_client(client_id)

    if not config:
        raise HTTPException(404, "Client not found")

    return {
        "client_id": client_id,
        "config": config
    }
