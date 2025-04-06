import json

from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["page"])
templates = Jinja2Templates(directory="app/templates")


def get_static_path(name: str):
    with open("./static/dist/.vite/manifest.json") as data:
        manifest = json.load(data)

    key = {
        "home": manifest["components/home/main.js"],
        "auth": manifest["components/auth/main.js"],
        "styles": manifest["../styles/main.css"],
    }

    return f"static/dist/{key[name]["file"]}"


def create_context(request: Request, title: str, root_id: str, react_script: str, extra: dict = {}):
    context = {
        "request": request,
        "title": title,
        "root_id": root_id,
        "react_script": react_script,
        "main_stylesheet": get_static_path("styles"),
    }

    context.update(extra)
    return context


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(
        "base.html", create_context(request, "Home", "homeDiv", get_static_path("home"))
    )


@router.get("/authenticate", response_class=HTMLResponse)
async def authenticate_page(request: Request):
    return templates.TemplateResponse(
        "base.html", create_context(request, "Authenticate", "authDiv", get_static_path("auth"))
    )
