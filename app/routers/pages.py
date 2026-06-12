from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.main_templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(request, "landing.html")
