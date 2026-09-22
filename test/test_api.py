import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/spend_tracker_test"
)

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield


def test_create_expense():
    response = client.post(
        "/expenses",
        json={
            "amount": 500,
            "category": "Food",
            "note": "Lunch",
            "date": "2026-09-21"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["amount"] == 500
    assert data["category"] == "Food"
    assert data["note"] == "Lunch"


def test_create_expense_with_invalid_amount():
    response = client.post(
        "/expenses",
        json={
            "amount": -100,
            "category": "Food",
            "note": "Invalid expense",
            "date": "2026-09-21"
        }
    )

    assert response.status_code == 422


def test_get_expenses():
    client.post(
        "/expenses",
        json={
            "amount": 500,
            "category": "Food",
            "note": "Lunch",
            "date": "2026-09-21"
        }
    )

    response = client.get("/expenses")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["category"] == "Food"


def test_filter_expenses_by_category():
    client.post(
        "/expenses",
        json={
            "amount": 500,
            "category": "Food",
            "date": "2026-09-21"
        }
    )

    client.post(
        "/expenses",
        json={
            "amount": 1000,
            "category": "Travel",
            "date": "2026-09-20"
        }
    )

    response = client.get("/expenses?category=Food")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["category"] == "Food"


def test_filter_expenses_by_date_range():
    client.post(
        "/expenses",
        json={
            "amount": 500,
            "category": "Food",
            "date": "2026-09-10"
        }
    )

    client.post(
        "/expenses",
        json={
            "amount": 1000,
            "category": "Travel",
            "date": "2026-09-20"
        }
    )

    response = client.get(
        "/expenses?start_date=2026-09-15&end_date=2026-09-25"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["category"] == "Travel"


def test_summary():
    client.post(
        "/expenses",
        json={
            "amount": 500,
            "category": "Food",
            "date": "2026-09-10"
        }
    )

    client.post(
        "/expenses",
        json={
            "amount": 1000,
            "category": "Travel",
            "date": "2026-09-20"
        }
    )

    response = client.get("/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total_spend"] == 1500
    assert data["spend_by_category"]["Food"] == 500
    assert data["spend_by_category"]["Travel"] == 1000