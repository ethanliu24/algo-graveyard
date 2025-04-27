from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from .middlewares import JWTCookieToHeaderMiddleware
from .pages import router as page_router
from .routes import api_router


app = FastAPI()
app.include_router(api_router)
app.add_middleware(JWTCookieToHeaderMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(page_router)


@app.exception_handler(404)
async def page_not_found(request: Request, exc_404: StarletteHTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=404, content={"detail": getattr(exc_404, "detail", "Not Found")})
    else:
      return RedirectResponse("/not-found")
