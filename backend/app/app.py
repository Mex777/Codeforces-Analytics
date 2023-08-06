import requests
from flask import Flask, request
from backend.app.config import DATABASE_CONNECTION_URL
from backend.app.extensions import db
from backend.app.models.models import User, Problem, Tag, Contest
from backend.app.models.tables import problem_tags, user_solved_problems
from backend.app.db_population import migrate_problems, migrate_users, migrate_contests, add_user_to_db, \
    get_user_solved_problems
from backend.app.predictor import predict_time_to_desired_rating
from backend.app.suggestion_api import user_based_collaborative_filtering

# creating the Flask app
app = Flask(__name__)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URL
db.init_app(app)

with app.app_context():
    db.create_all()
    # migrate_problems()
    # migrate_users()
    # migrate_contests()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/recommend/<user>")
def recommend(user):
    recommended_problems = user_based_collaborative_filtering(user)

    output = "<ul>"
    for curr_problem in recommended_problems:
        output += f"<li> {curr_problem.id} {curr_problem.rating} </li>"
    output += "</ul>"
    return output


@app.route("/predict/<handle>")
def predict(handle):
    if "rating" not in request.args.keys():
        return {
            "status": "FAILED",
            "message": "You should provide a desired rating"
        }

    days = predict_time_to_desired_rating(handle, request.args["rating"])
    return {
        "status": "SUCCESS",
        "time_in_days": days
    }, 200


@app.route("/problems/<handle>")
def user_solved_problems(handle):
    user_object = db.session.execute(db.select(User).where(User.handle == handle)).scalar()

    if user_object is None:
        return {"status": "FAILED", "message": "User not found"}, 404

    problems = user_object.toDict()["solved_problems"]

    return {"status": "SUCCESS", "problems_solved": problems}


@app.route("/users/<handle>", methods=["POST"])
def user(handle):
    user_object = db.session.execute(db.select(User).where(User.handle == handle)).scalar()
    if user_object is None:
        add_user_to_db(handle)
        return "SUCCESS", 200

    user_object.solved_problems = get_user_solved_problems(user_object.handle)
    db.session.commit()
    return "SUCCESS", 200
