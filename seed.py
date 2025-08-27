# Seed script that calls your running API to create a user, a class, and a booking.
# Run while the server is up: uvicorn app.main:app --reload
# Requires: pip install requests

import sys
import time
from datetime import datetime, timedelta
import requests

BASE_URL = "http://127.0.0.1:8000"

# Test data
ADMIN_NAME = "John Doe"
ADMIN_EMAIL = "john@example.com"
ADMIN_PASSWORD = "password123"

CLIENT_NAME = "Alice Johnson"
CLIENT_EMAIL = "alice@example.com"

def pretty(resp):
    try:
        return resp.status_code, resp.json()
    except Exception:
        return resp.status_code, resp.text

def ensure_user():
    print("==> Creating (or ensuring) user via /signup ...")
    resp = requests.post(f"{BASE_URL}/signup", json={
        "name": ADMIN_NAME,
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    })
    code, body = pretty(resp)
    print("Signup:", code, body)

def login():
    print("==> Logging in via /login ...")
    resp = requests.post(f"{BASE_URL}/login", json={
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    })
    code, body = pretty(resp)
    if code != 200 or "access_token" not in body:
        print("Login failed. Check your /login handler and credentials.")
        sys.exit(1)
    token = body["access_token"]
    print("Login:", code, {"token": token[:20] + "..."})
    return token

def create_class(token):
    print("==> Creating class via /classes ...")
    headers = {"Authorization": f"Bearer {token}"}
    future_time = (datetime.utcnow() + timedelta(days=30)).replace(microsecond=0).isoformat() + "Z"
    payload = {
        "name": "Morning Yoga",
        "dateTime": future_time,
        "instructor": "Jane Smith",
        "availableSlots": 20
    }
    resp = requests.post(f"{BASE_URL}/classes", headers=headers, json=payload)
    code, body = pretty(resp)
    if code not in (200, 201):
        print("Create class failed:", code, body)
        sys.exit(1)
    class_id = body.get("id") or body.get("class_id") or body.get("data", {}).get("id")
    print("Create class:", code, body)
    if not class_id:
        print("Could not detect class id from response; please check your /classes response schema.")
        sys.exit(1)
    return class_id

def create_booking(token, class_id):
    print("==> Creating booking via /bookings/ ...")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "class_id": class_id,
        "client_name": CLIENT_NAME,
        "client_email": CLIENT_EMAIL
    }
    resp = requests.post(f"{BASE_URL}/bookings/", headers=headers, json=payload)
    code, body = pretty(resp)
    print("Create booking:", code, body)

def list_classes():
    print("==> GET /classes ...")
    resp = requests.get(f"{BASE_URL}/classes")
    print("Classes:", pretty(resp))

def list_bookings(token):
    print("==> GET /bookings/ ...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/bookings/", headers=headers)
    print("Bookings:", pretty(resp))

if __name__ == "__main__":
    try:
        ensure_user()
        token = login()
        list_classes()
        cid = create_class(token)
        list_classes()
        create_booking(token, cid)
        list_bookings(token)
        print("\n✅ Seeding done.")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API at", BASE_URL, "- Is uvicorn running?")
        sys.exit(1)
