# backend/api/middleware/rate_limit_middleware.py

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from collections import defaultdict
from typing import Dict


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiter (per IP).
    Production ready for small–medium traffic.
    For high traffic, can be upgraded to Redis.
    """

    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds

        # Store: ip -> list[timestamps]
        self.request_log: Dict[str, list] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        request_times = self.request_log[client_ip]

        # Remove outdated timestamps
        request_times = [t for t in request_times if (current_time - t) < self.window_seconds]
        self.request_log[client_ip] = request_times

        if len(request_times) >= self.max_requests:
            retry_after = self.window_seconds - (current_time - request_times[0])
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too Many Requests - Rate limit exceeded",
                    "retry_after_seconds": round(retry_after, 2)
                }
            )

        # Log current request
        self.request_log[client_ip].append(current_time)

        # Continue request
        response = await call_next(request)
        return response
