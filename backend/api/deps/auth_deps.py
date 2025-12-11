# backend/api/deps/auth_deps.py
from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

def require_scope(scope: str):
    def _check(request: Request):
        meta = getattr(request.state, "client_meta", {}) or {}
        scopes = meta.get("scopes", [])
        if "*" in scopes:
            return True
        if scope not in scopes:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Insufficient scope")
        return True
    return _check
