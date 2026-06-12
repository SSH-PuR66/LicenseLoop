import hashlib
import secrets

from fastapi import Depends, HTTPException, Request
from itsdangerous import BadSignature, URLSafeTimedSerializer
from sqlmodel import Session

from app.config import settings
from app.database import get_session
from app.models import User

serializer = URLSafeTimedSerializer(settings.secret_key, salt="session")
SESSION_MAX_AGE = 60 * 60 * 24 * 14  # 14 days


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000).hex()
    return f"{salt}${digest}"


def verify_password(password: str, stored: str) -> bool:
    salt, digest = stored.split("$", 1)
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000).hex()
    return secrets.compare_digest(candidate, digest)


def create_session_token(user_id: int) -> str:
    return serializer.dumps({"uid": user_id})


def get_current_user(request: Request, session: Session = Depends(get_session)) -> User:
    token = request.cookies.get("session")
    if not token:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    try:
        data = serializer.loads(token, max_age=SESSION_MAX_AGE)
    except BadSignature:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    user = session.get(User, data["uid"])
    if not user:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user
