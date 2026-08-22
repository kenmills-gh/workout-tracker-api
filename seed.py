import datetime
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("🌱 Clearing out existing database tables...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("🏋️ Creating sample exercises...")
    pushups = Exercise(name="Push-ups", category="Strength", equipment_needed=False)
    bench_press = Exercise(
        name="Barbell Bench Press", category="Strength", equipment_needed=True
    )
    treadmill = Exercise(name="Treadmill Jog", category="Cardio", equipment_needed=True)

    db.session.add_all([pushups, bench_press, treadmill])
    db.session.commit()

    print("📅 Creating sample workouts...")
    workout_1 = Workout(
        date=datetime.date(2026, 8, 22),
        duration_minutes=45,
        notes="Upper body hyper-focus session.",
    )
    workout_2 = Workout(
        date=datetime.date(2026, 8, 25),
        duration_minutes=30,
        notes="Interval cardio and endurance.",
    )

    db.session.add_all([workout_1, workout_2])
    db.session.commit()

    print("🔗 Associating exercises with workouts (WorkoutExercises)...")
    we_1 = WorkoutExercise(
        workout_id=workout_1.id, exercise_id=pushups.id, sets=3, reps=15
    )
    we_2 = WorkoutExercise(
        workout_id=workout_1.id, exercise_id=bench_press.id, sets=4, reps=8
    )
    we_3 = WorkoutExercise(
        workout_id=workout_2.id, exercise_id=treadmill.id, duration_seconds=1800
    )

    db.session.add_all([we_1, we_2, we_3])
    db.session.commit()

    print("✅ Database seeding completed successfully!")
