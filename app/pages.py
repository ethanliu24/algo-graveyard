from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

def include_pages(app: FastAPI):
    @app.get("/", response_class=HTMLResponse)
    async def home_page(request: Request):
        return templates.TemplateResponse("base.html", create_context(request, "Home", "homeDiv", "TODO"))


def create_context(request: Request, title: str, root_id: str, react_script: str, extra: dict = {}):
    context = {
        "request": request,
        "title": title,
        "root_id": root_id,
        "react_script": react_script
    }

    context.update(extra)
    return context