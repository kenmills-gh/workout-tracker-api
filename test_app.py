import pytest
from app import app, db
from models import Exercise, Workout, WorkoutExercise
from datetime import date


@pytest.fixture
def client():
    # Configure app for testing with an in-memory SQLite database
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


# ==========================================
# MODEL VALIDATION TESTS
# ==========================================


def test_exercise_name_validation():
    """Test that creating an exercise with a name under 2 characters raises a ValueError."""
    with app.app_context():
        with pytest.raises(
            ValueError, match="Exercise name must be at least 2 characters long."
        ):
            Exercise(name="S", category="Strength")


def test_workout_notes_validation():
    """Test that notes exceeding 500 characters raise a ValueError."""
    with app.app_context():
        long_notes = "A" * 501
        with pytest.raises(ValueError, match="Notes cannot exceed 500 characters."):
            Workout(date=date(2026, 8, 22), notes=long_notes)


# ==========================================
# API ENDPOINT STATUS CODE & CRUD TESTS
# ==========================================


def test_get_exercises(client):
    """Test GET /exercises returns 200 and a list of exercises."""
    response = client.get("/exercises")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_create_exercise_success(client):
    """Test POST /exercises successfully creates an exercise and returns 201."""
    response = client.post(
        "/exercises",
        json={"name": "Pull-ups", "category": "Strength", "equipment_needed": True},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Pull-ups"
    assert data["id"] is not None


def test_create_exercise_invalid_name(client):
    """Test POST /exercises with a short name returns a 400 Bad Request."""
    response = client.post("/exercises", json={"name": "P", "category": "Strength"})
    assert response.status_code == 400


def test_get_workout_not_found(client):
    """Test GET /workouts/<id> returns 404 for a non-existent workout."""
    response = client.get("/workouts/999")
    assert response.status_code == 404


def test_create_workout_success(client):
    """Test POST /workouts successfully creates a workout record."""
    response = client.post(
        "/workouts",
        json={"date": "2026-08-22", "duration_minutes": 45, "notes": "Leg day focus."},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["duration_minutes"] == 45
    assert data["notes"] == "Leg day focus."
