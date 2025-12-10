# backend/agi/planning.py

from typing import List, Dict


class Planner:
    """
    Converts goals into step-by-step execution plans.
    """

    def create_plan(self, goal: Dict) -> List[Dict]:
        goal_type = goal.get("type", "generic")

        if goal_type == "sales":
            return [
                {"action": "collect_lead", "priority": 1},
                {"action": "send_brochure", "priority": 2},
                {"action": "schedule_site_visit", "priority": 3},
                {"action": "follow_up", "priority": 4},
            ]

        elif goal_type == "income":
            return [
                {"action": "launch_offer", "priority": 1},
                {"action": "run_whatsapp_campaign", "priority": 2},
                {"action": "close_deals", "priority": 3},
            ]

        else:
            return [
                {"action": "analyze_goal", "priority": 1},
                {"action": "execute_task", "priority": 2},
                {"action": "review_result", "priority": 3},
            ]
