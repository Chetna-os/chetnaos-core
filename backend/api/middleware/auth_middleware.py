# backend/api/middleware/auth_middleware.py
"""
Auth middleware for FastAPI:
- Validates X-API-KEY or Authorization: Bearer <key>
- Maps key -> client_id + metadata
- Enforces simple per-client allowed_routes (ACL)
- Minimal external dependencies (std lib + starlette)
- Config source: environment variable JSON string OR local file secrets/api_keys.json
"""

import os
import json
import logging
from typing import Dict, Optional, Any
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

logger = logging.getLogger("chetna.auth")
logger.setLevel(logging.INFO)


DEFAULT_KEYS_FILE = os.environ.get("CHETNA_API_KEYS_FILE", "secrets/api_keys.json")
# Optionally allow JSON in env var CHETNA_API_KEYS_JSON for quick deploy
ENV_KEYS_JSON = os.environ.get("CHETNA_API_KEYS_JSON", None)


def load_api_keys() -> Dict[str, Dict[str, Any]]:
    """
    Returns mapping: api_key -> metadata
    metadata example:
    {
       "client_id": "client_001",
       "active": True,
       "allowed_routes": ["/api/v1/chat", "/api/v1/goals"],
       "scopes": ["chat:write", "chat:read"]
    }
    """
    # 1) try env JSON
    if ENV_KEYS_JSON:
        try:
            data = json.loads(ENV_KEYS_JSON)
            logger.info("Loaded API keys from CHETNA_API_KEYS_JSON")
            return data
        except Exception as e:
            logger.error("Invalid CHETNA_API_KEYS_JSON: %s", e)

    # 2) try file
    if os.path.exists(DEFAULT_KEYS_FILE):
        try:
            with open(DEFAULT_KEYS_FILE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            logger.info("Loaded API keys from %s", DEFAULT_KEYS_FILE)
            return data
        except Exception as e:
            logger.error("Failed to read API keys file %s: %s", DEFAULT_KEYS_FILE, e)

    logger.warning("No API keys found; default empty map returned")
    return {}


class AuthError(Exception):
    pass


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, keys: Optional[Dict[str, Dict]] = None, enforce_acl: bool = True):
        super().__init__(app)
        # keys: api_key -> metadata
        self.keys = keys or load_api_keys()
        self.enforce_acl = enforce_acl

    def _extract_key(self, request: Request) -> Optional[str]:
        # Priority: X-API-KEY header -> Authorization: Bearer <key>
        key = request.headers.get("x-api-key")
        if key:
            return key.strip()
        auth = request.headers.get("authorization")
        if not auth:
            return None
        # support "Bearer <token>"
        parts = auth.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1].strip()
        return None

    def _unauthorized(self, msg="Unauthorized") -> Response:
        return JSONResponse({"detail": msg}, status_code=HTTP_401_UNAUTHORIZED)

    def _forbidden(self, msg="Forbidden") -> Response:
        return JSONResponse({"detail": msg}, status_code=HTTP_403_FORBIDDEN)

    async def dispatch(self, request: Request, call_next):
        # Allow open/public endpoints quickly (optional)
        # Example: skip auth for health check
        path = request.url.path
        if path in ("/health", "/metrics"):
            return await call_next(request)

        api_key = self._extract_key(request)
        if not api_key:
            return self._unauthorized("API key required")

        meta = self.keys.get(api_key)
        if not meta:
            logger.warning("Unknown API key attempt from %s path=%s", request.client.host, path)
            return self._unauthorized("Invalid API key")

        # Check active flag
        if not meta.get("active", True):
            logger.info("Inactive API key used: client=%s", meta.get("client_id"))
            return self._unauthorized("API key inactive")

        # ACL: allowed routes
        if self.enforce_acl:
            allowed = meta.get("allowed_routes")
            if allowed and not any(path.startswith(r) for r in allowed):
                logger.info("ACL deny for client=%s path=%s", meta.get("client_id"), path)
                return self._forbidden("Access to this endpoint is not allowed for your API key")

        # Attach client info into request.state for downstream handlers
        request.state.client_id = meta.get("client_id")
        request.state.client_meta = meta

        # Optional: rate-limit override per client (middleware can check request.state)
        # e.g. request.state.rate_limit = meta.get("rate_limit")

        # Logging
        logger.debug("Auth success client=%s path=%s", meta.get("client_id"), path)

        # Continue
        response = await call_next(request)
        # Optionally add header for debugging (do not expose sensitive data in prod)
        response.headers["X-Chetna-Client"] = meta.get("client_id", "unknown")
        return response
