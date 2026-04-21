"""
Automated tests for the Task Management API.
These tests use an isolated temporary SQLite database so that
coursework testing does not affect the main development database.
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db

TEST_DB_PATH = Path("test_tasks.db")
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

from main import app  # noqa: E402


def override_get_db():
    """Provide an isolated database session for API tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """Reset all database tables before each test for isolation."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_database():
    """Remove the temporary test database file when tests finish."""
    yield
    engine.dispose()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


def test_root_endpoint_returns_basic_api_information():
    """The root endpoint should confirm that the API is running."""
    response = client.get("/")
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "Task Management API is running."
    assert "timestamps" in data["features"]


def test_create_task_returns_201_and_created_record_with_timestamps():
    """Creating a task should return HTTP 201 and include timestamps."""
    payload = {
        "title": "Write coursework report",
        "description": "Document the API design and testing process",
        "completed": False,
        "due_date": "2026-05-10",
    }

    response = client.post("/api/tasks", json=payload)
    data = response.json()

    assert response.status_code == 201
    assert data["id"] >= 1
    assert data["title"] == payload["title"]
    assert data["completed"] is False
    assert "created_at" in data
    assert "updated_at" in data


def test_get_tasks_returns_paginated_structure():
    """The task list endpoint should return metadata and an items array."""
    client.post(
        "/api/tasks",
        json={
            "title": "Task one",
            "description": "First task",
            "completed": False,
            "due_date": "2026-05-11",
        },
    )

    response = client.get("/api/tasks?page=1&limit=5")
    data = response.json()

    assert response.status_code == 200
    assert data["page"] == 1
    assert data["limit"] == 5
    assert data["total"] == 1
    assert isinstance(data["items"], list)


def test_get_single_task_returns_200_for_existing_record():
    """The API should return an existing task when queried by ID."""
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Prepare slides",
            "description": "Create project presentation slides",
            "completed": False,
            "due_date": "2026-05-12",
        },
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/api/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_put_updates_full_task_record():
    """PUT should replace the full task payload for an existing task."""
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Initial title",
            "description": "Initial description",
            "completed": False,
            "due_date": "2026-05-15",
        },
    )
    task_id = create_response.json()["id"]

    update_payload = {
        "title": "Updated title",
        "description": "Updated description",
        "completed": True,
        "due_date": "2026-05-20",
    }
    response = client.put(f"/api/tasks/{task_id}", json=update_payload)

    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["completed"] is True


def test_patch_updates_only_selected_fields():
    """PATCH should update a subset of fields without replacing the entire record."""
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Patch me",
            "description": "Original description",
            "completed": False,
            "due_date": "2026-05-18",
        },
    )
    task_id = create_response.json()["id"]

    response = client.patch(f"/api/tasks/{task_id}", json={"completed": True})
    data = response.json()

    assert response.status_code == 200
    assert data["completed"] is True
    assert data["title"] == "Patch me"


def test_filtering_by_search_and_completion_status_works():
    """The list endpoint should support search and completed filters."""
    client.post(
        "/api/tasks",
        json={
            "title": "Searchable coursework task",
            "description": "Used for filter testing",
            "completed": True,
            "due_date": "2026-05-22",
        },
    )
    client.post(
        "/api/tasks",
        json={
            "title": "Another item",
            "description": "Different task",
            "completed": False,
            "due_date": "2026-05-23",
        },
    )

    response = client.get("/api/tasks?search=coursework&completed=true")
    data = response.json()

    assert response.status_code == 200
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Searchable coursework task"


def test_delete_returns_json_message():
    """Deleting a task should return a confirmation message in JSON format."""
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Delete me",
            "description": "This task will be removed",
            "completed": False,
            "due_date": "2026-05-25",
        },
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/api/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Task {task_id} deleted successfully"


def test_get_missing_task_returns_standardized_404_error():
    """A missing task ID should produce a standardized 404 error payload."""
    response = client.get("/api/tasks/999999")
    data = response.json()

    assert response.status_code == 404
    assert data["error"] == "HTTP error"
    assert data["detail"] == "Task not found"
    assert data["status_code"] == 404


def test_invalid_payload_returns_standardized_422_error():
    """Invalid request bodies should return the custom validation error format."""
    response = client.post(
        "/api/tasks",
        json={
            "title": "",
            "description": "Invalid task due to empty title",
            "completed": False,
            "due_date": "2026-05-26",
        },
    )
    data = response.json()

    assert response.status_code == 422
    assert data["error"] == "Validation error"
    assert data["status_code"] == 422
    assert isinstance(data["detail"], list)
