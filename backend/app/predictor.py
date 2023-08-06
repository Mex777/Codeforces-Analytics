from backend.app.extensions import db
from backend.app.models.models import RatingChange, Contest
from sqlalchemy import text
import numpy as np
from sklearn.linear_model import LinearRegression


def predict_time_to_desired_rating(handle, desired_rating):
    obj = db.session.query(RatingChange, Contest).join(RatingChange).where(RatingChange.user_handle == handle).all()

    if obj is None:
        return

    ratings = []
    time_from_beginning = [0]
    start_date = None

    for rt, c in obj:
        # print(rt.user_handle, rt.contest_id, rt.old_rating, rt.new_rating, c.date)

        if len(ratings) == 0:
            ratings.append(rt.new_rating)
            start_date = c.date

        if rt.new_rating >= ratings[len(ratings) - 1]:
            ratings.append(rt.new_rating)
            time_from_beginning.append((c.date - start_date).days)

    # print(ratings, time_from_beginning)
    ratings = np.array(ratings).reshape(-1, 1)
    time_from_beginning = np.array(time_from_beginning)

    model = LinearRegression()

    model.fit(ratings, time_from_beginning)

    r_sqr = model.score(ratings, time_from_beginning)

    days = model.predict(np.array([int(desired_rating)]).reshape(-1, 1))[0]
    days -= time_from_beginning[len(time_from_beginning) - 1]

    return days
