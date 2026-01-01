"""
ChetnaOS — app.py
-----------------
Single entry point of the ChetnaOS runtime.

Responsibilities:
- Initialize FastAPI
- Attach middleware
- Bind BrainRouterAdvanced
- Expose clean execution endpoint
- Serve frontend static files
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import logging
import time
import os

logger = logging.getLogger("ChetnaOS")
logging.basicConfig(level=logging.INFO)

# 🔌 LLM BOOTSTRAP (ONE TIME ONLY)
# Initialize LLM provider via bootstrap layer (explicit, no auto-registration)
from backend.bootstrap.llm_bootstrap import init_llm

try:
    init_llm()
except (ValueError, RuntimeError) as e:
    logger.warning(f"LLM Provider registration skipped: {e}")

from backend.orchestrator.brain_router_advanced import BrainRouterAdvanced
from backend.monitoring.health import health_check

app = FastAPI(title="ChetnaOS",
              version="0.9.0",
              description="AGI-ready cognitive operating system runtime")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

brain_router = BrainRouterAdvanced()


class ProcessRequest(BaseModel):
    input: str
    context: Dict[str, Any] | None = None


class ProcessResponse(BaseModel):
    status: str
    trace_id: str
    output: Dict[str, Any] | None = None
    reason: str | None = None


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
        result = brain_router.route(user_input=request.input,
                                    context=request.context or {})

        return ProcessResponse(status=result.get("status", "success"),
                               trace_id=result.get("trace_id"),
                               output=result.get("output"),
                               reason=result.get("reason"))

    except Exception as e:
        logger.exception("Fatal processing error")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def serve_frontend():
    """
    Serve the frontend index.html
    """
    return FileResponse("frontend/index.html")


app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.on_event("startup")
def on_startup():
    logger.info("ChetnaOS runtime started")


@app.on_event("shutdown")
def on_shutdown():
    logger.info("ChetnaOS runtime shutting down")


@app.post("/founder/approve/{trace_id}")
def founder_approve(trace_id: str):
    record = brain_router.founder_queue.approve(trace_id)

    if not record:
        return {"status": "not_found"}

    payload = record["payload"]

    # 🔁 Resume execution
    workflow = brain_router._select_workflow(payload["intent"])
    output = workflow.execute(user_input=payload["user_input"],
                              intent=payload["intent"],
                              context=payload["context"])

    return {
        "status": "approved_and_executed",
        "trace_id": trace_id,
        "output": output
    }
