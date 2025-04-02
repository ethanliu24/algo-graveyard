from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class JWTCookieToHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        print(request.headers)
        print(request.cookies.get("jwt_token"))
        return response
