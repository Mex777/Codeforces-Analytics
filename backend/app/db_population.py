import json
import time
from datetime import datetime
import requests

from backend.app.models.models import User, Problem, Tag, Contest, RatingChange
from backend.app.extensions import db


def get_user_solved_problems(handle):
    response = requests.get(f"https://codeforces.com/api/user.status?handle={handle}").json()
    solved_problems = set()

    # going through each submission of the current user
    for submission in response["result"]:
        # if the user has solved the problem and the problem was part of a contest
        if submission["verdict"] == "OK" and "contestId" in submission.keys() and "rating" in submission["problem"].keys():
            # the problem ID is the concatenation between the contestID of the problem, and it's index
            problem_id = str(submission["contestId"]) + submission["problem"]["index"]

            problem_object = db.session.execute(db.select(Problem).where(Problem.id == problem_id)).scalar()
            if problem_object is None:
                problem_object = add_problem_to_db(submission["problem"])

            solved_problems.add(problem_object)

    return list(solved_problems)


def add_user_to_db(handle, user_json=None):
    if user_json is None:
        request = requests.get(f"https://codeforces.com/api/user.info?handles={handle}")
        print(request.json())
        if request.status_code != 200:
            raise RuntimeError("Codeforces not available")

        user_json = request.json()
        if user_json["status"] == "FAILED":
            raise NameError("User not found")
        user_json = user_json["result"][0]

    rating = user_json["rating"]
    max_rating = user_json["maxRating"]
    profile_pic = user_json["avatar"]
    rank = user_json["rank"]
    solved_problems = get_user_solved_problems(handle)

    user_object = User(handle, rating, max_rating, profile_pic, rank)
    db.session.add(user_object)
    user_object.solved_problems = solved_problems

    db.session.commit()
    return user_object


def add_problem_to_db(problem_json):
    problem_id = str(problem_json["contestId"]) + problem_json["index"]

    if "rating" not in problem_json.keys():
        return

    problem_rating = problem_json["rating"]
    problem_tags = problem_json["tags"]

    problem_obj = Problem(problem_id, problem_json["name"], problem_rating)
    db.session.add(problem_obj)

    # Populating the tags
    for curr_tag in problem_tags:
        existing_tag = db.session.execute(db.select(Tag).where(Tag.name == curr_tag)).scalar()
        # if the current tag is not in the database we add it
        if existing_tag is None:
            tag_obj = Tag(curr_tag)
            db.session.add(tag_obj)
        else:
            tag_obj = existing_tag

        # we add the current tag to the problem
        if tag_obj not in problem_obj.tags:
            problem_obj.tags.append(tag_obj)

    db.session.commit()
    return problem_obj


def add_contest_to_db(contest_json):
    if (contest_json["type"] == "CF" and contest_json["phase"] == "FINISHED") is False:
        return

    date = datetime.fromtimestamp(int(contest_json["startTimeSeconds"]))
    contest_obj = Contest(int(contest_json["id"]), contest_json["name"], date)
    db.session.add(contest_obj)

    # adding the rating changes
    resp = requests.get(f"https://codeforces.com/api/contest.ratingChanges?contestId={contest_obj.id}").json()
    for rating_change_obj in resp["result"]:
        handle = rating_change_obj["handle"]
        old_rating = rating_change_obj["oldRating"]
        new_rating = rating_change_obj["newRating"]

        user_obj = db.session.execute(db.select(User).where(User.handle == handle)).scalar()
        if user_obj is None:
            add_user_to_db(handle)

        rating_change = RatingChange(handle, contest_obj.id, old_rating, new_rating)
        db.session.add(rating_change)

    db.session.commit()
    return contest_obj


def migrate_users():
    response = requests.get("https://codeforces.com/api/user.ratedList?activeOnly=true&includeRetired=false")
    length = len(response["result"])
    # to delete, it helps to understand the progress
    cnt = 0
    for curr_user in response["result"]:
        cnt += 1

        # pausing for a second at each step to avoid overloading the public API from codeforces
        time.sleep(1)

        # to delete
        # if cnt == 1000:
        #     break
        print(str(cnt) + " / " + str(length))

        handle = curr_user["handle"]
        existing_user = db.session.execute(db.select(User).where(User.handle == handle)).scalar()
        if existing_user is None:
            add_user_to_db(handle, curr_user)
        else:
            existing_user.solved_problems = get_user_solved_problems(handle)
            db.session.commit()


def migrate_problems():
    response = requests.get("https://codeforces.com/api/problemset.problems").json()

    for problem in response["result"]["problems"]:
        problem_id = str(problem["contestId"]) + problem["index"]
        existing_problem = db.session.execute(db.select(Problem).where(Problem.id == problem_id)).scalar()
        if existing_problem is None:
            add_problem_to_db(problem)


def migrate_contests():
    response = requests.get("https://codeforces.com/api/contest.list").json()

    for curr_contest in response["result"]:
        add_contest_to_db(curr_contest)
