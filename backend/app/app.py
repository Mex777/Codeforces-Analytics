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


def create_app(database_url):
    # creating the Flask app
    app = Flask(__name__)

    # configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    db.init_app(app)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/recommend/<user>")
    def recommend(user):
        try:
            recommended_problems = user_based_collaborative_filtering(user)

            return {
                "status": "SUCCESS",
                "recommended_problems": [problem.toDict() for problem in recommended_problems]
            }
        except:
            return {
                "status": "FAILED",
                "message": "An error has occurred, try again later"
            }, 500

    @app.route("/predict/<handle>")
    def predict(handle):
        if "rating" not in request.args.keys():
            return {
                "status": "FAILED",
                "message": "You should provide a desired rating"
            }, 401

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
            try:
                add_user_to_db(handle)
                return "SUCCESS", 200
            except NameError as error:
                return str(error), 404
            except RuntimeError as error:
                return str(error), 500

        try:
            user_object.solved_problems = get_user_solved_problems(user_object.handle)
            db.session.commit()
            return "SUCCESS", 200
        except:
            return "CODEFORCES NOT AVAILABLE", 500

    return app


if __name__ == "__main__":
    app = create_app(DATABASE_CONNECTION_URL)

    with app.app_context():
        db.create_all()
        migrate_problems()
        migrate_users()
        migrate_contests()

    app.run()
