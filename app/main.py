from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .middlewares import JWTCookieToHeaderMiddleware
from .pages import include_pages
from .routes import api_router


app = FastAPI()
app.include_router(api_router)
app.add_middleware(JWTCookieToHeaderMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
include_pages(app)
