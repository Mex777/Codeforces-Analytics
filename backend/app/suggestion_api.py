import time
import requests
import json

from backend.app.db_population import add_user_to_db
from backend.app.extensions import db
from backend.app.models.models import User, Problem


def user_based_collaborative_filtering(handle):

    target_user_db_object = db.session.execute(db.select(User).where(User.handle == handle)).scalar()
    if target_user_db_object is None:
        target_user_db_object = add_user_to_db(handle)

    target_solved_problems = [problem.id for problem in target_user_db_object.solved_problems]
    users = db.session.execute(db.select(User).where(
        (User.handle != handle) & ((target_user_db_object.rating + 200) >= User.rating) & (User.rating >= (target_user_db_object.rating - 200))).limit(5000)).scalars()


    # Step 1: Calculate implicit user similarity
    similarities = {}
    for user in users:
        solved_problems = user.solved_problems

        # Calculate Jaccard similarity as a measure of implicit similarity
        common_problems = set(solved_problems) & set(target_solved_problems)
        similarity = len(common_problems) / (len(solved_problems) + len(target_solved_problems) - len(common_problems))
        similarities[user.handle] = similarity

    # Step 2: Identify nearest neighbors (similar users)
    nearest_neighbors = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:20]

    # Step 3: Aggregate weights from nearest neighbors' solved problems
    aggregated_weights = {}
    for neighbor, similarity in nearest_neighbors:
        neighbor_object = db.session.execute(db.select(User).where(User.handle == neighbor)).scalar()
        for problem in neighbor_object.solved_problems:
            if problem.id not in target_solved_problems:
                aggregated_weights.setdefault(problem, 0)
                aggregated_weights[problem] += similarity

    # Step 4: Filter and rank recommended problems

    recommended_problems = []
    for problem in aggregated_weights.keys():
        if (target_user_db_object.rating - 400) < problem.rating < (target_user_db_object.rating + 400):
            recommended_problems.append(problem)

            if len(recommended_problems) == 20:
                break

    recommended_problems = sorted(recommended_problems, key=lambda x: aggregated_weights[x], reverse=True)

    return recommended_problems
