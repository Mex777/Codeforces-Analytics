from backend.app.extensions import db
from backend.app.models.tables import problem_tags, user_solved_problems, user_contests


class User(db.Model):
    __tablename__ = 'Users'

    handle = db.Column(db.String(255), primary_key=True)
    rating = db.Column(db.Integer)
    max_rating = db.Column(db.Integer)
    profile_pic = db.Column(db.String(255))
    rank = db.Column(db.String(50))

    # Define the many-to-many relationship with SolvedProblem table
    solved_problems = db.relationship('Problem', secondary=user_solved_problems, back_populates='solvers')

    # Define the many-to-many relationship with Contest table
    contests = db.relationship('Contest', secondary=user_contests, back_populates='participants')

    def __init__(self, handle, rating, max_rating, profile_pic, rank):
        self.handle = handle
        self.rating = rating;
        self.max_rating = max_rating
        self.profile_pic = profile_pic
        self.rank = rank


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


class Tag(db.Model):
    __tablename__ = 'Tags'

    name = db.Column(db.String(255), primary_key=True)

    # Define the many-to-many relationship with Problem table
    problems = db.relationship('Problem', secondary=problem_tags, back_populates='tags')

    def __init__(self, name):
        self.name = name


class Contest(db.Model):
    __tablename__ = 'Contest'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date = db.Column(db.TIMESTAMP)

    # Define the many-to-many relationship with User table (participants)
    participants = db.relationship('User', secondary=user_contests, back_populates='contests')

    def __init__(self, id, name, date):
        self.id = id
        self.name = name
        self.date = date
