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
import uuid

logger = logging.getLogger("ChetnaOS")
logging.basicConfig(level=logging.INFO)

# Import health check (lightweight, reload-safe)
from monitoring.health import health_check

# Create FastAPI app instance (must be at module level for ASGI)
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

# Lazy-load heavy components to avoid reload issues
# These are initialized in startup event, not at module level
brain_router = None


def format_response(raw_result: Any, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Unified response formatter.
    
    Converts raw agent/workflow results into a consistent API response structure.
    Handles various response formats: dict, str, nested structures.
    
    Args:
        raw_result: Raw result from brain router, agent, or workflow
        context: Optional context dict containing trace_id, intent, etc.
    
    Returns:
        {
            "success": bool,
            "message": str,  # Human-readable reply (always present)
            "intent": str,   # Detected intent (if available)
            "agent": str,    # Agent/workflow name (if available)
            "trace_id": str, # Request trace ID (if available)
            "raw": Any       # Original raw result (optional, for debugging)
        }
    """
    context = context or {}
    
    # Extract message text from various possible structures
    message_text = None
    intent = None
    agent_name = "custom"
    trace_id = context.get("trace_id")
    
    if isinstance(raw_result, dict):
        # Check for direct message fields (priority order)
        message_text = (
            raw_result.get("message") or
            raw_result.get("reply") or
            raw_result.get("text") or
            raw_result.get("response")
        )
        
        # Check nested output structure
        if not message_text and "output" in raw_result:
            output = raw_result["output"]
            if isinstance(output, dict):
                message_text = (
                    output.get("message") or
                    output.get("reply") or
                    output.get("text") or
                    output.get("response")
                )
            elif isinstance(output, str):
                message_text = output
        
        # Extract metadata
        intent = raw_result.get("intent") or context.get("intent")
        agent_name = (
            raw_result.get("agent") or
            raw_result.get("workflow") or
            raw_result.get("output", {}).get("workflow") if isinstance(raw_result.get("output"), dict) else None
        ) or "custom"
        
        trace_id = raw_result.get("trace_id") or trace_id
        
        # Check for error/blocked status
        status = raw_result.get("status", "").lower()
        if status in ["blocked", "error", "failed"]:
            message_text = message_text or raw_result.get("reason") or "Request was blocked or failed"
            return {
                "success": False,
                "message": message_text,
                "intent": intent,
                "agent": agent_name,
                "trace_id": trace_id,
                "raw": raw_result if logger.level <= logging.DEBUG else None
            }
    
    elif isinstance(raw_result, str):
        message_text = raw_result
    
    # Fallback: convert to string if no message found
    if not message_text:
        if raw_result:
            message_text = str(raw_result)
        else:
            message_text = "No response generated"
    
    # Ensure message is a string and not empty
    if not isinstance(message_text, str):
        message_text = str(message_text)
    
    if not message_text.strip():
        message_text = "Request processed successfully"
    
    # Clean up message (remove common artifacts)
    message_text = message_text.strip()
    
    return {
        "success": True,
        "message": message_text,
        "intent": intent,
        "agent": agent_name,
        "trace_id": trace_id,
        "raw": raw_result if logger.level <= logging.DEBUG else None
    }


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


@app.post("/process")
async def process(request: ProcessRequest):
    """
    Main cognitive execution endpoint.
    Returns normalized response with clear text reply.
    """
    try:
        context = request.context or {}
        context["trace_id"] = str(uuid.uuid4())
        
        if not request.input or not request.input.strip():
            return format_response(
                {"status": "error", "reason": "Input text is required"},
                context
            )

        # Lazy-load brain router if not initialized
        global brain_router
        if brain_router is None:
            try:
                from orchestrator.brain_router_advanced import BrainRouterAdvanced
                brain_router = BrainRouterAdvanced()
            except Exception as e:
                logger.error(f"Failed to initialize brain router: {e}")
                return format_response(
                    {"status": "error", "reason": "System initialization error. Please try again."},
                    context
                )

        # Route through brain router
        result = brain_router.route(
            user_input=request.input,
            context=context
        )

        # Format response using unified formatter
        return format_response(result, context)

    except Exception as e:
        logger.exception("Fatal processing error")
        error_context = context if 'context' in locals() else {}
        return format_response(
            {"status": "error", "reason": f"Error processing request: {str(e)}"},
            error_context
        )


@app.get("/")
async def serve_frontend():
    """
    Serve the frontend index.html
    """
    return FileResponse("frontend/index.html")


app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.on_event("startup")
def on_startup():
    """
    Initialize heavy components on startup (reload-safe).
    This avoids module-level side effects that can break uvicorn reload.
    """
    global brain_router
    
    logger.info("ChetnaOS runtime starting...")
    
    # 🔌 LLM BOOTSTRAP (ONE TIME ONLY)
    # Initialize LLM provider via bootstrap layer (explicit, no auto-registration)
    try:
        from bootstrap.llm_bootstrap import init_llm
        init_llm()
        logger.info("LLM provider registered via bootstrap")
    except (ValueError, RuntimeError, ImportError) as e:
        logger.warning(f"LLM Provider registration skipped: {e}")
        # Fallback: try direct registration if bootstrap fails
        try:
            from integrations.llm import LLMRegistry
            from integrations.llm.groq_provider import GroqProvider
            LLMRegistry.register(GroqProvider({}))
            logger.info("LLM provider registered via fallback")
        except Exception as fallback_error:
            logger.warning(f"Fallback LLM registration also failed: {fallback_error}")
    
    # Initialize brain router (heavy component, lazy-loaded)
    try:
        from orchestrator.brain_router_advanced import BrainRouterAdvanced
        brain_router = BrainRouterAdvanced()
        logger.info("BrainRouterAdvanced initialized")
    except Exception as e:
        logger.error(f"Failed to initialize BrainRouterAdvanced: {e}")
        # Create a minimal fallback router to prevent crashes
        brain_router = None
    
    logger.info("ChetnaOS runtime started")


@app.on_event("shutdown")
def on_shutdown():
    logger.info("ChetnaOS runtime shutting down")


@app.post("/founder/approve/{trace_id}")
def founder_approve(trace_id: str):
    """
    Founder approval endpoint for pending actions.
    """
    try:
        # Lazy-load brain router if not initialized
        global brain_router
        if brain_router is None:
            return {
                "status": "error",
                "message": "Brain router not initialized"
            }
        
        if not brain_router.founder_queue:
            return {
                "status": "error",
                "message": "Founder queue not available"
            }

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
    except Exception as e:
        logger.exception("Error in founder approval")
        return {
            "status": "error",
            "message": str(e)
        }


# ASGI entry point guard for direct execution
# When running: python backend/app.py, backend/ is in sys.path, so use "app:app"
if __name__ == "__main__":
    import uvicorn
    # Use string format for ASGI app specification (reload-safe)
    # Since backend/ is in sys.path when running python backend/app.py, use "app:app"
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )