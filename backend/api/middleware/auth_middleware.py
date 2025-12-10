from fastapi import Request, HTTPException

async def auth_middleware(request: Request, call_next):
    api_key = request.headers.get("x-api-key")

    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    # Demo ke liye static key
    if api_key != "CHETNA-CLIENT-KEY":
        raise HTTPException(status_code=403, detail="Invalid API key")

    response = await call_next(request)
    return response
