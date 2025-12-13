# backend/config/settings.py

import os
from pathlib import Path


# -------------------------------------------------
# Core Paths
# -------------------------------------------------

BASE_DIR = Path(_file_).resolve().parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"
CLIENT_PROJECTS_DIR = BASE_DIR / "client_projects"


# -------------------------------------------------
# Environment
# -------------------------------------------------

ENVIRONMENT = os.getenv("CHETNA_ENV", "development")
DEBUG = ENVIRONMENT != "production"


# -------------------------------------------------
# Security
# -------------------------------------------------

SECRET_KEY = os.getenv("CHETNA_SECRET_KEY", "chetna-dev-secret")
API_KEY_HEADER = "X-CHETNA-API-KEY"


# -------------------------------------------------
# Client System
# -------------------------------------------------

MULTI_TENANT_ENABLED = True
CLIENT_ISOLATION_ENABLED = True


# -------------------------------------------------
# AGI / AUTONOMY CONTROLS
# -------------------------------------------------

AUTONOMY_LEVEL = int(os.getenv("CHETNA_AUTONOMY_LEVEL", 1))
# 0 = manual
# 1 = assisted
# 2 = semi-autonomous
# 3 = autonomous (future)


FOUNDER_IN_LOOP = True
SELF_MODIFICATION_ALLOWED = False


# -------------------------------------------------
# Resource / Physics Limits
# -------------------------------------------------

MAX_ACTIONS_PER_MINUTE = 60
MAX_MEMORY_MB_PER_CLIENT = 256
ENERGY_BUDGET_PER_DAY = 1000  # abstract units


# -------------------------------------------------
# Logging
# -------------------------------------------------

LOG_LEVEL = os.getenv("CHETNA_LOG_LEVEL", "INFO")
ENABLE_REQUEST_LOGGING = True


# -------------------------------------------------
# Feature Flags
# -------------------------------------------------

FEATURE_FLAGS = {
    "scientific_laws_engine": True,
    "self_reprogrammable_core": False,
    "time_loop_awareness": False,
    "physical_interaction": False,
}
