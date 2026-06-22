---
title: "I Built a License Expiration Tracker That Emails You Before Things Expire — FastAPI + Stripe + Docker"
published: false
description: "LicenseLoop tracks business licenses, sends automated reminders at 30/7/1 days before expiration, and handles Pro upgrades via Stripe. Full-stack Python."
tags: python, fastapi, saas, docker
cover_image: ""
canonical_url:
---

Nobody thinks about business licenses until they expire. Then it's a scramble — fees, penalties, sometimes suspended operations. I built **LicenseLoop** to solve a boring but real problem: track expiration dates and automatically email reminders before things go bad.

It's not glamorous. It's not AI. But it's the kind of tool that actual businesses would pay for, and building it taught me more about production Python than any tutorial.

---

## What it does

1. You create an account (JWT-based auth with bcrypt)
2. You add your licenses — business license, health permit, fire inspection, whatever
3. LicenseLoop shows a dashboard with color-coded expiration status
4. Background tasks send email reminders at 30 days, 7 days, and 1 day before expiration
5. Free tier gets 5 licenses, Pro tier ($X/mo via Stripe) gets unlimited

---

## Architecture

```
FastAPI + Uvicorn
├── SQLModel + SQLite (zero-config database)
├── Stripe Checkout + Webhooks (billing)
├── SMTP Mailer (background task alerts)
├── Jinja2 Templates (dashboard UI)
└── Docker + Docker Compose (deployment)
```

### Why FastAPI?

- **Async-native** — email sending and Stripe calls don't block the server
- **Pydantic/SQLModel** — one model class serves as both the API schema and the database table
- **Automatic docs** — OpenAPI spec generated for free at `/docs`
- **Lifespan events** — `init_db()` runs on startup, database is ready before the first request

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="LicenseLoop", version="1.0.0", lifespan=lifespan)
```

### Why SQLite?

For a single-tenant app with a few hundred licenses, SQLite is perfect. No server to manage, no connection strings, no Docker container for the database. The file lives on disk and SQLModel handles the ORM.

When (if) you need to scale, the SQLModel code transfers to PostgreSQL with a connection string change. That's the beauty of an ORM — you don't rewrite queries.

---

## The reminder system

The background task processor checks daily for licenses approaching expiration:

- **30 days out** — "heads up, this is coming"
- **7 days out** — "you should start the renewal process"
- **1 day out** — "this expires tomorrow"

The SMTP mailer sends through whatever provider you configure — Mailtrap for dev, SendGrid for production, or any SMTP server.

This is the kind of feature that separates "student project" from "could actually be a product." Anyone can build a CRUD form. The value is in the automation that runs when nobody's looking.

---

## Stripe integration

The billing flow:

1. User clicks "Upgrade to Pro"
2. Backend creates a Stripe Checkout Session
3. User pays via Stripe's hosted payment page
4. Stripe sends a webhook to `/api/billing/webhook`
5. Backend validates the webhook signature, upgrades the user's plan

```python
@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    event = stripe.Webhook.construct_event(payload, sig, webhook_secret)

    if event.type == "checkout.session.completed":
        # Upgrade user to Pro
        ...
```

The webhook signature validation is critical — without it, anyone could POST fake events to your webhook endpoint and give themselves a free upgrade.

---

## Testing

```bash
pytest
```

The test suite covers the core license management logic — CRUD operations, expiration calculations, and authentication flows. Tests run against an in-memory SQLite instance so they're fast and isolated.

---

## Docker deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker-compose up --build
```

One command and you're running. The Docker Compose setup handles the app container and any supporting services.

---

## What I learned

1. **Background tasks are where the value lives.** The CRUD part of this app took a day. The reminder system is what makes it useful, and it took the most thought — timing, deduplication, email templates, error handling.
2. **Stripe webhooks are security-critical.** Always validate the signature. Always handle duplicate events (idempotency). Always log webhook processing for debugging.
3. **SQLite is fine.** The internet wants you to use Postgres for everything. For a single-service app with predictable data patterns, SQLite removes an entire class of operational concerns.
4. **Boring problems are good portfolio pieces.** An AI chatbot is cool but competitive. A license tracker is boring but shows you can build something a real business would use.

---

*Source: [github.com/SSH-PuR66/LicenseLoop](https://github.com/SSH-PuR66/LicenseLoop)*
