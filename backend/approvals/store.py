from typing import Dict
from .models import ApprovalRequest, ApprovalStatus

_APPROVAL_STORE: Dict[str, ApprovalRequest] = {}


def add_approval(req: ApprovalRequest):
    _APPROVAL_STORE[req.id] = req
    return req.id


def get_pending():
    return [
        r for r in _APPROVAL_STORE.values()
        if r.status == ApprovalStatus.PENDING
    ]


def get_by_id(approval_id: str):
    return _APPROVAL_STORE.get(approval_id)


def update_status(approval_id: str, status: ApprovalStatus):
    if approval_id in _APPROVAL_STORE:
        _APPROVAL_STORE[approval_id].status = status
        return True
    return False
