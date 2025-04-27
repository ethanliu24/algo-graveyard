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
        "create": manifest["components/create/main.js"],
        "question": manifest["components/question/main.js"],
        "about": manifest["components/about/main.js"],
        "not_found": manifest["components/not_found/main.js"],
        "styles": manifest["../styles/main.css"],
    }

    return f"{key[name]["file"]}"


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


@router.get("/admin", response_class=HTMLResponse)
async def authenticate_page(request: Request):
    return templates.TemplateResponse(
        "base.html", create_context(request, "Authenticate", "authDiv", get_static_path("auth"))
    )


@router.get("/create", response_class=HTMLResponse)
async def question_creation_page(request: Request):
    return templates.TemplateResponse(
        "base.html", create_context(request, "Create", "createDiv", get_static_path("create"))
    )


@router.get("/questions/{question_id}", response_class=HTMLResponse)
async def question_page(request: Request, question_id: str):
    return templates.TemplateResponse(
        "base.html", create_context(request, f"{question_id}", "questionDiv", get_static_path("question"))
    )


@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse(
        "base.html", create_context(request, "About", "aboutDiv", get_static_path("about"))
    )


@router.get("/not-found", response_class=HTMLResponse)
async def not_found_page(request: Request):
    return templates.TemplateResponse(
        "base.html", create_context(request, "Not Found", "notFoundDiv", get_static_path("not_found"))
    )
