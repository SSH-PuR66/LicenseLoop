from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select

from app.auth import get_current_user
from app.config import settings
from app.database import get_session
from app.main_templates import templates
from app.models import License, User

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: User = Depends(get_current_user),
                    session: Session = Depends(get_session)):
    licenses = session.exec(
        select(License).where(License.user_id == user.id).order_by(License.expires_on)
    ).all()
    today = date.today()
    rows = [{"license": lic, "days_left": (lic.expires_on - today).days} for lic in licenses]
    at_limit = user.plan == "free" and len(licenses) >= settings.free_plan_limit
    return templates.TemplateResponse(request, "dashboard.html", {
        "user": user, "rows": rows, "at_limit": at_limit,
        "free_limit": settings.free_plan_limit,
        "expiring_soon": sum(1 for r in rows if 0 <= r["days_left"] <= 30),
        "overdue": sum(1 for r in rows if r["days_left"] < 0),
        "error": request.query_params.get("error"),
    })


@router.post("/licenses")
async def create_license(name: str = Form(...), authority: str = Form(""),
                         license_number: str = Form(""), expires_on: date = Form(...),
                         notes: str = Form(""), user: User = Depends(get_current_user),
                         session: Session = Depends(get_session)):
    count = len(session.exec(select(License).where(License.user_id == user.id)).all())
    if user.plan == "free" and count >= settings.free_plan_limit:
        return RedirectResponse("/dashboard?error=limit", status_code=303)
    session.add(License(user_id=user.id, name=name, authority=authority,
                        license_number=license_number, expires_on=expires_on, notes=notes))
    session.commit()
    return RedirectResponse("/dashboard", status_code=303)


@router.post("/licenses/{license_id}/delete")
async def delete_license(license_id: int, user: User = Depends(get_current_user),
                         session: Session = Depends(get_session)):
    lic = session.get(License, license_id)
    if lic and lic.user_id == user.id:
        session.delete(lic)
        session.commit()
    return RedirectResponse("/dashboard", status_code=303)
