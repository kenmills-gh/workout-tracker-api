from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
import datetime

app = Flask(__name__)

# Configure the SQLite database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# Initialize Schemas
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()


# ==========================================
# WORKOUT ENDPOINTS
# ==========================================


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return jsonify(workout_schema.dump(workout)), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    json_data = request.get_json()
    try:
        # Schema validation & deserialization
        data = workout_schema.load(json_data)

        # Ensure date is parsed correctly if passed as a string
        workout_date = data.get("date")
        if isinstance(workout_date, str):
            workout_date = datetime.datetime.strptime(workout_date, "%Y-%m-%d").date()

        new_workout = Workout(
            date=workout_date,
            duration_minutes=data.get("duration_minutes"),
            notes=data.get("notes"),
        )
        db.session.add(new_workout)
        db.session.commit()
        return jsonify(workout_schema.dump(new_workout)), 201

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database constraint violation."}), 400


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted successfully"}), 200


# ==========================================
# EXERCISE ENDPOINTS
# ==========================================


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return jsonify(exercise_schema.dump(exercise)), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    json_data = request.get_json()
    try:
        data = exercise_schema.load(json_data)

        new_exercise = Exercise(
            name=data.get("name"),
            category=data.get("category"),
            equipment_needed=data.get("equipment_needed", False),
        )
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(new_exercise)), 201

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Exercise name must be unique."}), 400


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted successfully"}), 200


# ==========================================
# WORKOUT-EXERCISES (JOIN) ENDPOINTS
# ==========================================


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    # Verify both parent entities exist
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)

    json_data = request.get_json() or {}
    try:
        data = workout_exercise_schema.load(json_data, partial=True)

        new_we = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds"),
        )
        db.session.add(new_we)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(new_we)), 201

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database constraint violation."}), 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
