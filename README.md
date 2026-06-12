# LicenseLoop

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![SQLModel](https://img.shields.io/badge/SQLModel-008080?style=for-the-badge&logo=python)](https://sqlmodel.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![Stripe](https://img.shields.io/badge/Stripe-008FC7?style=for-the-badge&logo=stripe&logoColor=white)](https://stripe.com)

LicenseLoop is a licensing expiration tracking system. Built with FastAPI, SQLModel (SQLite), and Stripe, it provides a clean dashboard to monitor renewal dates, send automated email alerts, and handle user plans.

---

## Key Features

- **Async FastAPI Engine**: Built for speed and clean route handling.
- **Secure Authentication**: JWT-based session security with bcrypt password hashing.
- **Interactive Dashboard**: Visual indicators tracking active licenses, days left to renew, overdue warnings, and limits.
- **Stripe Subscription Integration**: Fully functional stripe checkout and webhooks to auto-manage Pro upgrades.
- **Dockerized Architecture**: Dev-ready multi-stage Dockerfile and Docker Compose configurations.
- **Background Email Alerts**: Background task processor configured for SMTP mailer notifications.

---

## System Architecture

- **Backend Framework**: FastAPI (Python 3.11+)
- **Database / ORM**: SQLModel + SQLite
- **Payments / Billing**: Stripe checkout session & webhook validation
- **Deployment Platform**: Docker & Docker Compose

---

## Setup & Execution

### 1. Configuration (.env)

Create a `.env` file in the root directory:

```env
# App Configuration
SECRET_KEY="supersecretjwtkeychangeinproduction"
APP_URL="http://localhost:8000"

# Stripe Configuration
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_PRICE_ID="price_..."
STRIPE_WEBHOOK_SECRET="whsec_..."

# SMTP Configuration
SMTP_HOST="smtp.mailtrap.io"
SMTP_PORT=2525
SMTP_USER="smtp-username"
SMTP_PASSWORD="smtp-password"
FROM_EMAIL="alerts@licenseloop.com"
```

### 2. Manual Run

Set up a Python virtual environment and run locally:

```bash
# Set up environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch dev server
uvicorn app.main:app --reload
```

Open `http://localhost:8000` to start using LicenseLoop.

### 3. Docker Compose Run

Spin up the entire container stack instantly:

```bash
docker-compose up --build
```

---

## Running Tests

To run the testing suite, execute:

```bash
pytest
```

---

## License

Distributed under the MIT License. See LICENSE for more information.
