from fastapi import FastAPI
from .middlewares import JWTCookieToHeaderMiddleware
from .routes import api_router

app = FastAPI()
app.include_router(api_router)
app.add_middleware(JWTCookieToHeaderMiddleware)
