# 🏋️ Workout Tracker API

A robust backend REST API built with **Flask**, **SQLAlchemy**, and **Marshmallow** designed to manage workouts, custom exercises, and performance tracking (sets, reps, and durations) through a many-to-many relationship structure.

---

## 🛠️ Tech Stack & Tools
* **Language:** Python 
* **Framework:** Flask, Flask-SQLAlchemy, Flask-Migrate
* **Validation & Serialization:** Marshmallow
* **Database:** SQLite
* **Environment Management:** Pipenv

---

## 🚀 Getting Started & Installation

1. **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd workout-tracker-api
2. **Install Dependencies:**
    ```bash
    pipenv install
    pipenv shell
3. **Run DB migrations:**
    ```bash
    flask db upgrade head
4. **Seed the DB with sample data:**
    ```bash
    python seed.py
5. **Run the local development server:**
    ```bash
    python app.py
    ```
    The server will run locally at http://127.0.0.1:5555.
---

## 🔌 API Endpoints Reference
### Workouts
* GET /workouts - Retrieve a list of all recorded workouts.

* GET /workouts/<id> - Retrieve a single workout with nested exercises and set details.

* POST /workouts - Create a new workout.

* DELETE /workouts/<id> - Delete a workout (cascades to join records).

### Exercises
* GET /exercises - Retrieve all available exercises.

* GET /exercises/<id> - Retrieve a specific exercise.

* POST /exercises - Create a new exercise (enforces unique names and minimum length validations).

* DELETE /exercises/<id> - Delete an exercise.

### Workout-Exercises (Join Table)
* POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Link an exercise to a workout with performance stats (sets, reps, duration_seconds).
---

## 🛡️ Validation & Constraints
* Model & Schema Validations: Enforces character length restrictions on names and notes, and prevents negative values for durations, sets, and reps using Marshmallow and SQLAlchemy validators.

* Error Handling: Returns structured JSON error responses with appropriate HTTP status codes (400 Bad Request, 404 Not Found) when constraints or validation rules are violated.