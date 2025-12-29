from enum import Enum
from typing import Dict, Any
from datetime import datetime
import uuid


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEFERRED = "deferred"


class ApprovalRequest:

    def __init__(self, trace_id: str, intent: str, user_input: str,
                 wisdom_reason: str, context: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.trace_id = trace_id
        self.intent = intent
        self.user_input = user_input
        self.reason = wisdom_reason
        self.context = context
        self.status = ApprovalStatus.PENDING
        self.created_at = datetime.utcnow().isoformat()
