from fastapi import APIRouter, HTTPException
from agents.sales_agent import SalesAgent
from agents.whatsapp_agent import WhatsAppAgent
from agents.custom_agent import CustomAgent

router = APIRouter(prefix="/agents", tags=["Agents"])

# Agent registry
AGENT_CLASSES = {
    "sales": SalesAgent,
    "whatsapp": WhatsAppAgent,
    "custom": CustomAgent
}

@router.post("/{agent_type}")
async def run_agent(agent_type: str, payload: dict):
    """
    Run any agent (Sales / WhatsApp / Custom)
    """
    if agent_type not in AGENT_CLASSES:
        raise HTTPException(status_code=400, detail="Invalid agent type")

    text = payload.get("text")
    context = payload.get("context", {})

    agent = AGENT_CLASSES[agent_type](client_id=context.get("client_id"))
    result = await agent.process(text, context)

    return {
        "agent_type": agent_type,
        "result": result
    }
