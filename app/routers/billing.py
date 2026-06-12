import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.auth import get_current_user
from app.config import settings
from app.database import get_session
from app.models import User

router = APIRouter(prefix="/billing")
stripe.api_key = settings.stripe_secret_key


@router.post("/checkout")
async def checkout(user: User = Depends(get_current_user)):
    session_obj = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": settings.stripe_price_id, "quantity": 1}],
        customer_email=user.email,
        success_url=f"{settings.app_url}/dashboard?upgraded=1",
        cancel_url=f"{settings.app_url}/dashboard",
        metadata={"user_id": str(user.id)},
    )
    return RedirectResponse(session_obj.url, status_code=303)


@router.post("/webhook")
async def webhook(request: Request, session: Session = Depends(get_session)):
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, signature, settings.stripe_webhook_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="Invalid webhook")

    if event["type"] == "checkout.session.completed":
        data = event["data"]["object"]
        user = session.get(User, int(data["metadata"]["user_id"]))
        if user:
            user.plan = "pro"
            user.stripe_customer_id = data.get("customer")
            session.add(user)
            session.commit()
    elif event["type"] == "customer.subscription.deleted":
        customer_id = event["data"]["object"]["customer"]
        user = session.exec(select(User).where(User.stripe_customer_id == customer_id)).first()
        if user:
            user.plan = "free"
            session.add(user)
            session.commit()
    return {"received": True}
