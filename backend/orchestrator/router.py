from backend.orchestrator.intent_detector import IntentDetector
from backend.orchestrator.priority_engine import PriorityEngine

from backend.agents.sales_agent import SalesAgent
from backend.agents.whatsapp_agent import WhatsAppAgent
from backend.agents.custom_agent import CustomAgent
from backend.agi.goal_agent import GoalAgent


class BrainRouter:
    """
    Core AGI Brain Router of ChetnaOS.
    """

    def __init__(self):
        self.intent_detector = IntentDetector()
        self.priority_engine = PriorityEngine()

        # Agent registry
        self.agent_registry = {
            "sales": SalesAgent,
            "chat": CustomAgent,
            "goal": GoalAgent,
            "support": WhatsAppAgent
        }

    async def route(self, text: str, context: dict = None):
        """
        Selects correct agent based on intent and priority.
        """
        context = context or {}

        # 1️⃣ Detect intent
        intent = self.intent_detector.detect(text)

        # 2️⃣ Load correct agent
        agent_class = self.agent_registry.get(intent, CustomAgent)

        agent = agent_class(client_id=context.get("client_id"))

        # 3️⃣ Execute agent safely
        try:
            result = await agent.process(text, context)
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback": "System temporarily unavailable."
            }

        return {
            "intent": intent,
            "priority": self.priority_engine.get_priority(intent),
            "result": result
        }
