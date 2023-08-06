# from backend.app.extensions import db
from backend.app.extensions import db

# Association Table for Many-to-Many Relationship between Problems and Tags
problem_tags = db.Table('Problem_Tags',
                        db.Column('problem_id', db.String(255), db.ForeignKey('Problems.id', ondelete='CASCADE'), primary_key=True),
                        db.Column('tag_name', db.String(255), db.ForeignKey('Tags.name', ondelete='CASCADE'), primary_key=True)
                        )

# Association Table for Many-to-Many Relationship between Users and Solved_Problems
user_solved_problems = db.Table('User_Solved_Problems',
                                db.Column('user_handle', db.String(255), db.ForeignKey('Users.handle', ondelete='CASCADE'), primary_key=True),
                                db.Column('problem_id', db.String(255), db.ForeignKey('Problems.id', ondelete='CASCADE'), primary_key=True)
                                )
