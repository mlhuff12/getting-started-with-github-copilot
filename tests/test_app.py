from fastapi.testclient import TestClient
import sys
import os
from urllib.parse import quote

# Ensure the src directory is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "tester@example.com"
    encoded_activity = quote(activity, safe="")

    # Sign up
    resp = client.post(f"/activities/{encoded_activity}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant added
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email in resp.json()[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{encoded_activity}/participants?email={email}")
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")

    # Verify participant removed
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email not in resp.json()[activity]["participants"]
