import os
from datetime import date, timedelta

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient

from app.database import init_db
from app.main import app

client = TestClient(app)
init_db()


def signup_and_login():
    client.post("/signup", data={"email": "owner@shop.com", "password": "supersecret1"})
    res = client.post("/login", data={"email": "owner@shop.com", "password": "supersecret1"},
                      follow_redirects=False)
    assert res.status_code == 303


def test_landing():
    assert client.get("/").status_code == 200


def test_auth_and_license_flow():
    signup_and_login()
    expires = (date.today() + timedelta(days=20)).isoformat()
    res = client.post("/licenses", data={"name": "Food Permit", "expires_on": expires},
                      follow_redirects=False)
    assert res.status_code == 303
    res = client.get("/dashboard")
    assert "Food Permit" in res.text


def test_free_plan_limit():
    expires = (date.today() + timedelta(days=90)).isoformat()
    for i in range(4):
        client.post("/licenses", data={"name": f"Permit {i}", "expires_on": expires})
    res = client.get("/dashboard?error=limit")
    assert "limited to" in res.text


def test_cron_endpoint_requires_secret():
    assert client.post("/tasks/send-reminders").status_code == 403
