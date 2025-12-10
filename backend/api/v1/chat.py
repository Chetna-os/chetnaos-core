from fastapi import APIRouter, HTTPException
from backend.orchestrator.router import BrainRouter

router = APIRouter(prefix="/chat", tags=["Chat"])

brain = BrainRouter()

@router.post("/")
async def chat_endpoint(payload: dict):
    """
    Universal conversational entry point.
    Automatically selects right agent based on intent.
    """
    text = payload.get("text")
    context = payload.get("context", {})

    if not text:
        raise HTTPException(400, "Text is required")

    response = await brain.route(text, context)

    return {
        "success": True,
        "response": response
    }
