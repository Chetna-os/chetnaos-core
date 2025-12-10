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
