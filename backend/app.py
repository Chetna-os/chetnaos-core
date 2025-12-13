"""
ChetnaOS — app.py
-----------------
Single entry point of the ChetnaOS runtime.

Responsibilities:
- Initialize FastAPI
- Attach middleware
- Bind BrainRouterAdvanced
- Expose clean execution endpoint
- Keep AGI logic OUT of this file
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import logging
import time

# --------------------------------------------------
# Core Orchestration
# --------------------------------------------------
from backend.orchestrator.brain_router_advanced import BrainRouterAdvanced

# --------------------------------------------------
# Middleware
# --------------------------------------------------
from backend.api.middleware.logging_middleware import logging_middleware
from backend.api.middleware.auth_middleware import auth_middleware
from backend.api.middleware.rate_limit_middleware import rate_limit_middleware

# --------------------------------------------------
# Monitoring
# --------------------------------------------------
from backend.monitoring.health import health_check

# --------------------------------------------------
# App Initialization
# --------------------------------------------------
app = FastAPI(
    title="ChetnaOS",
    version="0.9.0",
    description="AGI-ready cognitive operating system runtime"
)

logger = logging.getLogger("ChetnaOS")
logging.basicConfig(level=logging.INFO)

# --------------------------------------------------
# Middleware Wiring
# --------------------------------------------------
app.middleware("http")(logging_middleware)
app.middleware("http")(auth_middleware)
app.middleware("http")(rate_limit_middleware)

# --------------------------------------------------
# Brain Router (SINGLE INSTANCE)
# --------------------------------------------------
brain_router = BrainRouterAdvanced()

# --------------------------------------------------
# Request / Response Models
# --------------------------------------------------
class ProcessRequest(BaseModel):
    input: str
    context: Dict[str, Any] | None = None


class ProcessResponse(BaseModel):
    status: str
    trace_id: str
    output: Dict[str, Any] | None = None
    reason: str | None = None


# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.get("/health")
def health():
    """
    Runtime health & readiness probe
    """
    return health_check()


@app.post("/process", response_model=ProcessResponse)
def process(request: ProcessRequest):
    """
    Main cognitive execution endpoint
    """
    start_time = time.time()

    try:
        result = brain_router.route(
            user_input=request.input,
            context=request.context or {}
        )

        return ProcessResponse(
            status=result.get("status", "success"),
            trace_id=result.get("trace_id"),
            output=result.get("output"),
            reason=result.get("reason")
        )

    except Exception as e:
        logger.exception("Fatal processing error")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# Boot Marker (IMPORTANT for AGI autonomy later)
# --------------------------------------------------
@app.on_event("startup")
def on_startup():
    logger.info("🟢 ChetnaOS runtime started")


@app.on_event("shutdown")
def on_shutdown():
    
    logger.info("🔴 ChetnaOS runtime shutting down")
