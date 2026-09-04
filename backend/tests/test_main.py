import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ["DATABASE_PATH"] = "./test_workout.db"

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_log_and_history(client):
    log_entry = {
        "date": "2026-09-04",
        "day": 1,
        "exercise_index": 0,
        "exercise_name": "bench_press",
        "kg": 60.0,
    }
    create_response = client.post("/log", json=log_entry)
    assert create_response.status_code == 200
    assert create_response.json()["exercise_name"] == "bench_press"

    history_response = client.get("/history", params={"exercise_name": "bench_press"})
    assert history_response.status_code == 200
    assert len(history_response.json()) >= 1
