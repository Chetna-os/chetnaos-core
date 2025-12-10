from fastapi import FastAPI
from backend.api.middleware.logging_middleware import logging_middleware
from backend.api.middleware.auth_middleware import auth_middleware
from backend.api.middleware.rate_limit_middleware import rate_limit_middleware

app = FastAPI(title="ChetnaOS API")

app.middleware("http")(logging_middleware)
app.middleware("http")(auth_middleware)
app.middleware("http")(rate_limit_middleware)
# backend/agi/goal_agent.py

from typing import Dict, Any
from backend.agi.planning import Planner
from backend.agi.reflection_loop import ReflectionLoop
from backend.agi.world_state import WorldState


class GoalAgent:
    """
    Autonomous Goal Execution Controller of ChetnaOS.
    """

    def _init_(self):
        self.planner = Planner()
        self.reflector = ReflectionLoop()
        self.world = WorldState()

    async def run_goal(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Full AGI loop:
        Goal → Plan → Execute → Reflect → Update World
        """

        plan = self.planner.create_plan(goal)

        execution_results = []

        for step in plan:
            result = await self._execute_step(step)
            execution_results.append(result)

            reflection = self.reflector.reflect(step, result)

            # Learning impact on world state
            if result.get("income"):
                self.world.record_income(result["income"])

        return {
            "goal": goal,
            "plan": plan,
            "results": execution_results,
            "final_world_state": self.world.snapshot()
        }

    async def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fake executor for now — later connect real agents here
        """
        action = step.get("action")

        if action == "collect_lead":
            self.world.add_lead({"source": "whatsapp", "status": "new"})
            return {"success": True}

        elif action == "close_deals":
            self.world.record_income(50000)  # Sample income
            return {"success": True, "income": 50000}

        else:
            return {"success": True}
# quick test snippet (run with python -m asyncio)
import asyncio
from backend.agents.sale_agent import SalesAgent

async def main():
    a = SalesAgent(client_id="demo", config={"project_info": {"name": "Kalpavriksha", "min_price": "25 Lakhs"}})
    r = await a.process("Hi, kitna price hai?", {})
    print(r)

asyncio.run(main())
      from backend.scientific_laws.law_engine import ScientificLawEngine

law_engine = ScientificLawEngine()
