from flask import Flask
from backend.app.config import DATABASE_CONNECTION_URL
from backend.app.extensions import db
from backend.app.models.models import User, Problem, Tag, Contest
from backend.app.models.tables import problem_tags, user_solved_problems, user_contests

# creating the Flask app
app = Flask(__name__)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URL
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
