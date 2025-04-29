from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from .env_vars import ENV_VARS
from .middlewares import JWTCookieToHeaderMiddleware
from .pages import router as page_router
from .routes import api_router


app = FastAPI()
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(page_router)


app.add_middleware(JWTCookieToHeaderMiddleware)

allow_origins = ["http://127.0.0.1:8000", "http://0.0.0.0"]
prod_domain = ENV_VARS.get("PROD_DOMAIN", "")
if prod_domain != "": allow_origins.append(prod_domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or "*" for all (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(404)
async def page_not_found(request: Request, exc_404: StarletteHTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=404, content={"detail": getattr(exc_404, "detail", "Not Found")})
    else:
      return RedirectResponse("/not-found")
