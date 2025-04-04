from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .middlewares import JWTCookieToHeaderMiddleware
from .pages import router as page_router
from .routes import api_router


app = FastAPI()
app.include_router(api_router)
app.add_middleware(JWTCookieToHeaderMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(page_router)
