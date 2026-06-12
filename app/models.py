from datetime import date, datetime, timezone

from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    plan: str = "free"  # "free" or "pro"
    stripe_customer_id: str | None = None
    created_at: datetime = Field(default_factory=utcnow)


class License(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    name: str
    authority: str = ""        # e.g. "City of Austin"
    license_number: str = ""
    expires_on: date
    notes: str = ""
    created_at: datetime = Field(default_factory=utcnow)
