# backend/agents/scheduler_agent.py
"""
SchedulerAgent: schedules calls/visits & returns structured payloads.
This is lightweight; integration with task-queues (RQ/Celery/Temporal) can be added.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
from .base_agent import BaseAgent

class SchedulerAgent(BaseAgent):
    def _init_(self, client_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super()._init_(name="SchedulerAgent", client_id=client_id, config=config)

    async def handle(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # naive parse: look for "tomorrow", "today", "dd-mm" etc.
        ctx = context or {}
        user = ctx.get("user_name", "Client")
        # default: schedule next available 2pm tomorrow
        now = datetime.utcnow()
        scheduled_at = now + timedelta(days=1)
        scheduled_at = scheduled_at.replace(hour=14, minute=0, second=0, microsecond=0)
        # you'd parse actual date/time from text in production (use dateparser)
        job = {
            "type": "site_visit",
            "scheduled_at": scheduled_at.isoformat(),
            "organizer": "SalesTeam",
            "user": user,
            "notes": text[:300]
        }
        # In production: push this job to queue or calendar API
        # example: await task_queue.enqueue("send_visit_confirmation", job)
        self.update_state("last_schedule", job)
        return {"response": f"Site visit scheduled on {scheduled_at.date()} at 14:00 (tentative).", "job": job}
