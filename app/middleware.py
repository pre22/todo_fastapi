from fastapi import Request

async def log_middleware(request: Request, call_next):
    print(f"{request.method} {request.url}")
    response = await call_next(request)
    return response
