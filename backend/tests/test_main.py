import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = "./test_workout.db"
os.environ["DATABASE_PATH"] = DB_PATH

import pytest
from fastapi.testclient import TestClient

from database import engine
from main import app


@pytest.fixture(scope="session", autouse=True)
def clean_db():
    yield
    engine.dispose()
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_log_returns_201(client):
    log_entry = {
        "date": "2026-09-04",
        "day": 1,
        "exercise_index": 0,
        "exercise_name": "bench_press",
        "kg": 60.0,
    }
    response = client.post("/log", json=log_entry)
    assert response.status_code == 201
    assert response.json()["exercise_name"] == "bench_press"


def test_history_returns_list_for_known_exercise(client):
    log_entry = {
        "date": "2026-09-04",
        "day": 1,
        "exercise_index": 0,
        "exercise_name": "squat",
        "kg": 100.0,
    }
    client.post("/log", json=log_entry)

    response = client.get("/history", params={"exercise_name": "squat"})
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 1
    assert body[0]["exercise_name"] == "squat"
