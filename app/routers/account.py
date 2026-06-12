from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select

from app.auth import SESSION_MAX_AGE, create_session_token, hash_password, verify_password
from app.database import get_session
from app.main_templates import templates
from app.models import User

router = APIRouter()


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(request, "signup.html", {"error": None})


@router.post("/signup")
async def signup(request: Request, email: str = Form(...), password: str = Form(...),
                 session: Session = Depends(get_session)):
    email = email.strip().lower()
    if len(password) < 8:
        return templates.TemplateResponse(request, "signup.html",
                                          {"error": "Password must be at least 8 characters."})
    if session.exec(select(User).where(User.email == email)).first():
        return templates.TemplateResponse(request, "signup.html",
                                          {"error": "That email is already registered."})
    user = User(email=email, password_hash=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return _login_redirect(user.id)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None})


@router.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...),
                session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == email.strip().lower())).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(request, "login.html",
                                          {"error": "Invalid email or password."})
    return _login_redirect(user.id)


@router.post("/logout")
async def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("session")
    return response


def _login_redirect(user_id: int) -> RedirectResponse:
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("session", create_session_token(user_id), max_age=SESSION_MAX_AGE,
                        httponly=True, samesite="lax")
    return response
