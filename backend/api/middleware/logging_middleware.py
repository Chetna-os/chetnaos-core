# backend/api/middleware/logging_middleware.py

import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Configure logger
logger = logging.getLogger("chetna.logging")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs:
    - request path
    - method
    - client IP
    - request size
    - status code
    - execution time
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        try:
            request_body = await request.body()
            body_size = len(request_body) if request_body else 0
        except Exception:
            body_size = 0

        logger.info(
            f"Incoming Request → {request.method} {request.url.path} "
            f"(size={body_size} bytes, client={request.client.host})"
        )

        try:
            response: Response = await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled server error: {str(e)}", exc_info=True)
            raise e

        process_time = (time.time() - start_time) * 1000

        logger.info(
            f"Response → {request.method} {request.url.path} | "
            f"Status={response.status_code} | Time={process_time:.2f}ms"
        )

        return response
