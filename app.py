from flask import Flask
from flask_migrate import Migrate
from models import db

app = Flask(__name__)

# Configure the SQLite database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout_tracker.db"
# Disable modification tracking to save resources
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the SQLAlchemy instance with the app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(port=5555, debug=True)
