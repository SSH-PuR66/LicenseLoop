from datetime import date, timedelta

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlmodel import Session, select

from app.config import settings
from app.database import get_session
from app.models import License, User
from app.services.emailer import send_email

router = APIRouter(prefix="/tasks")
REMINDER_DAYS = (30, 7, 1)


@router.post("/send-reminders")
async def send_reminders(x_cron_secret: str = Header(""),
                         session: Session = Depends(get_session)):
    if x_cron_secret != settings.cron_secret:
        raise HTTPException(status_code=403, detail="Forbidden")

    today = date.today()
    sent = 0
    for days in REMINDER_DAYS:
        target = today + timedelta(days=days)
        for lic in session.exec(select(License).where(License.expires_on == target)).all():
            user = session.get(User, lic.user_id)
            if user:
                send_email(
                    user.email,
                    f"⏰ {lic.name} expires in {days} day{'s' if days > 1 else ''}",
                    f"Your '{lic.name}' ({lic.authority}) expires on {lic.expires_on}.\n"
                    f"Renew it now to avoid fines or downtime.\n\n— LicenseLoop",
                )
                sent += 1
    return {"reminders_sent": sent}
