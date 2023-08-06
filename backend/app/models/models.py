from backend.app.extensions import db
from backend.app.models.tables import problem_tags, user_solved_problems


class User(db.Model):
    __tablename__ = 'Users'

    handle = db.Column(db.String(255), primary_key=True)
    rating = db.Column(db.Integer)
    max_rating = db.Column(db.Integer)
    profile_pic = db.Column(db.String(255))
    rank = db.Column(db.String(50))

    # Define the many-to-many relationship with SolvedProblem table
    solved_problems = db.relationship('Problem', secondary=user_solved_problems, back_populates='solvers')

    def __init__(self, handle, rating, max_rating, profile_pic, rank):
        self.handle = handle
        self.rating = rating;
        self.max_rating = max_rating
        self.profile_pic = profile_pic
        self.rank = rank

    def toDict(self):
        return {
            "handle": self.handle,
            "rating": self.rating,
            "max_rating": self.max_rating,
            "profile_pic": self.profile_pic,
            "rank": self.rank,
            "solved_problems": [problem.toDict() for problem in self.solved_problems]
        }


class Problem(db.Model):
    __tablename__ = 'Problems'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    rating = db.Column(db.Integer)

    # Define the many-to-many relationship with Tag table
    tags = db.relationship('Tag', secondary=problem_tags, back_populates='problems')

    # Define the many-to-many relationship with User table (solvers)
    solvers = db.relationship('User', secondary=user_solved_problems, back_populates='solved_problems')

    def __init__(self, id, name, rating):
        self.id = id
        self.name = name
        self.rating = rating

    def toDict(self):
        return {"id": self.id, "name": self.name, "rating": self.rating, "tags": [tag.name for tag in self.tags]}


class Tag(db.Model):
    __tablename__ = 'Tags'

    name = db.Column(db.String(255), primary_key=True)

    # Define the many-to-many relationship with Problem table
    problems = db.relationship('Problem', secondary=problem_tags, back_populates='tags')

    def __init__(self, name):
        self.name = name

    def toDict(self):
        return {
            "name": self.name,
            "problems": [problem.toDict() for problem in self.problems]
        }


class Contest(db.Model):
    __tablename__ = 'Contest'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date = db.Column(db.DateTime)

    def __init__(self, id, name, date):
        self.id = id
        self.name = name
        self.date = date

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date
        }


class RatingChange(db.Model):
    __tablename__ = 'Rating_Change'

    user_handle = db.Column(db.String(255), db.ForeignKey(User.handle, ondelete='CASCADE'), primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey(Contest.id, ondelete='CASCADE'), primary_key=True)
    old_rating = db.Column(db.Integer)
    new_rating = db.Column(db.Integer)

    def __init__(self, user_handle, contest_id, old_rating, new_rating):
        self.user_handle = user_handle
        self.contest_id = contest_id
        self.old_rating = old_rating
        self.new_rating = new_rating

    def toDict(self):
        return {
            "user_handle": self.user_handle,
            "contest_id": self.contest_id,
            "old_rating": self.old_rating,
            "new_rating": self.new_rating
        }
