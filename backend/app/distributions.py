import requests

from backend.app.extensions import db
from backend.app.models.models import User

rating = {}
problems = {}


def rating_distrib():
    if len(rating.keys()) > 0:
        return rating

    response = requests.get("https://codeforces.com/api/user.ratedList?activeOnly=true&includeRetired=false").json()
    total = 0
    for curr_user in response["result"]:
        curr_rating = curr_user["rating"] - (curr_user["rating"] % 100)

        if curr_rating not in rating:
            rating[curr_rating] = 0
        rating[curr_rating] += 1
        total += 1

    temp_total = 0
    for curr_rating in rating.keys():
        rating[curr_rating] = round(rating[curr_rating] / total * 100, 2)
        temp_total += rating[curr_rating]

    print(temp_total)

    return rating


def problems_distrib():
    if len(problems.keys()) > 0:
        return problems

    user_object = db.session.execute(db.select(User)).scalars().all()
    for user in user_object:
        for solved_problem in user.solved_problems:
            if solved_problem.rating not in rating.keys():
                problems[solved_problem.rating] = 0

            problems[solved_problem.rating] += 1

    for curr_rating in problems.keys():
        problems[curr_rating] = (problems[curr_rating] + len(user_object) - 1) // len(user_object)

    return problems


