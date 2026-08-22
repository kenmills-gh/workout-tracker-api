from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    # Table Constraint: Prevent negative workout durations in the DB
    __table_args__ = (
        CheckConstraint("duration_minutes >= 0", name="check_duration_positive"),
    )

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan"
    )

    # Model Validation: Ensure notes aren't excessively long
    @validates("notes")
    def validate_notes(self, key, notes):
        if notes and len(notes) > 500:
            raise ValueError("Notes cannot exceed 500 characters.")
        return notes

    def __repr__(self):
        return f"<Workout {self.id} on {self.date}>"


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    # Table Constraint: 'unique=True' ensures no duplicate exercise names
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan"
    )

    # Model Validation: Ensure exercise name is provided and is at least 2 characters
    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name) < 2:
            raise ValueError("Exercise name must be at least 2 characters long.")
        return name

    def __repr__(self):
        return f"<Exercise {self.name}>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Table Constraints: Reps and sets cannot be negative
    __table_args__ = (
        CheckConstraint("reps >= 0", name="check_reps_positive"),
        CheckConstraint("sets >= 0", name="check_sets_positive"),
    )

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    # Model Validation: duration_seconds cannot be negative
    @validates("duration_seconds")
    def validate_duration(self, key, duration_seconds):
        if duration_seconds is not None and duration_seconds < 0:
            raise ValueError("Duration in seconds cannot be negative.")
        return duration_seconds

    def __repr__(self):
        return (
            f"<WorkoutExercise Workout:{self.workout_id} Exercise:{self.exercise_id}>"
        )
