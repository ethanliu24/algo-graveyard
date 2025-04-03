from fastapi import Request, Header
from starlette.middleware.base import BaseHTTPMiddleware

class JWTCookieToHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        jwt_token = request.cookies.get("jwt_token")
        if jwt_token:
            auth_header: tuple[bytes, bytes] = b"authorization", f"Bearer {jwt_token}".encode()
            request.headers.__dict__["_list"].append(auth_header)

        return await call_next(request)
