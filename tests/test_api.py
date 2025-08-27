import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Fitness Studio Booking API" in response.json()["message"]

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_signup():
    response = client.post(
        "/auth/signup",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_login():
    # First signup
    client.post(
        "/auth/signup",
        json={
            "name": "Login Test",
            "email": "login@example.com",
            "password": "testpassword123"
        }
    )
    
    # Then login
    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"