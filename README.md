# 🔄 LicenseLoop

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![SQLModel](https://img.shields.io/badge/SQLModel-008080?style=for-the-badge&logo=python)](https://sqlmodel.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![Stripe](https://img.shields.io/badge/Stripe-008FC7?style=for-the-badge&logo=stripe&logoColor=white)](https://stripe.com)

**LicenseLoop** is a production-ready, lightning-fast licensing expiration tracking system. Built on FastAPI, SQLModel (SQLite), and Stripe, it gives you a clean visual dashboard to monitor renewal dates, send automated email alerts, and manage subscription limits seamlessly.

---

## 🔥 Key Features

- **⚡ High-Performance API**: Fully async backend powered by FastAPI.
- **🛡️ Secure Authentication**: JWT-based session security with bcrypt password hashing.
- **📅 Expiration Dashboard**: Real-time tracking of license status, days remaining, and visual indicators for overdue or expiring assets.
- **💳 Stripe Subscription Integration**: Complete checkouts, webhooks, and automatic plan upgrading/downgrading.
- **🐳 Containerized Dev Environment**: Multi-stage Docker setup with Docker Compose.
- **🔔 Automatic Alerts**: Background tasks with email notifications for upcoming expirations.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **Database / ORM**: SQLModel, SQLite
- **Styling / UI**: Vanilla CSS / HTML Templates (Tailwind-ready structure)
- **Payments**: Stripe API & Webhooks
- **Deployment**: Docker & Docker Compose

---

## ⚙️ Quick Start

### 1. Environment Configuration

Clone this repository and create a `.env` file in the root directory:

```bash
# App Configs
SECRET_KEY="supersecretjwtkeychangeinproduction"
APP_URL="http://localhost:8000"

# Stripe Configs
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_PRICE_ID="price_..."
STRIPE_WEBHOOK_SECRET="whsec_..."

# Email Server (SMTP)
SMTP_HOST="smtp.mailtrap.io"
SMTP_PORT=2525
SMTP_USER="smtp-username"
SMTP_PASSWORD="smtp-password"
FROM_EMAIL="alerts@licenseloop.com"
```

### 2. Local Setup (Without Docker)

Create a virtual environment and install requirements:

```bash
# Create virtual env
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

Open your browser to `http://localhost:8000` to access the application.

### 3. Containerized Setup (With Docker)

Simply run:

```bash
docker-compose up --build
```

---

## 🔒 Stripe Integration Details

To test the payment pipeline locally, use the Stripe CLI to forward webhooks to your local server:

```bash
stripe listen --forward-to localhost:8000/billing/webhook
```

Copy the printed webhook secret (`whsec_...`) and update your `.env` file.

---

## 🧪 Testing

To run the test suite:

```bash
pytest
```

---

## 📄 License

This project is licensed under the MIT License.
