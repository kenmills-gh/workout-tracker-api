from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(
            min=2, error="Exercise name must be at least 2 characters long."
        ),
    )
    category = fields.Str(allow_none=True)
    equipment_needed = fields.Bool()

    class Meta:
        ordered = True


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)

    # allow_none=True allows null values for fields that don't apply to every exercise type
    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0, error="Reps cannot be negative."),
    )
    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0, error="Sets cannot be negative."),
    )
    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0, error="Duration in seconds cannot be negative."),
    )

    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    class Meta:
        ordered = True


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0, error="Duration in minutes cannot be negative."),
    )
    notes = fields.Str(
        allow_none=True,
        validate=validate.Length(max=500, error="Notes cannot exceed 500 characters."),
    )

    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema), dump_only=True
    )

    class Meta:
        ordered = True
