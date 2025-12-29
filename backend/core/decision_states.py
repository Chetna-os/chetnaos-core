"""
Decision States — System-wide Authority
--------------------------------------
Every cognitive layer MUST obey these states.
No local enums allowed beyond this.
"""

from enum import Enum


class DecisionState(Enum):
    ALLOW = "allow"
    ALLOW_WITH_WARNING = "allow_with_warning"
    DEFER = "defer"
    REQUIRE_FOUNDER = "require_founder"
    REJECT = "reject"
    SAFE_MODE = "safe_mode"
