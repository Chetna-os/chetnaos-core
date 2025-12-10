import time
from fastapi import Request, HTTPException

REQUEST_LIMIT = 60   # 60 requests per minute
user_requests = {}

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()

    request_log = user_requests.get(client_ip, [])
    request_log = [t for t in request_log if current_time - t < 60]

    if len(request_log) >= REQUEST_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")

    request_log.append(current_time)
    user_requests[client_ip] = request_log

    response = await call_next(request)
    return response
