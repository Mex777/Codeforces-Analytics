from flask import Flask
from config import DATABASE_CONNECTION_URL
from flask_sqlalchemy import SQLAlchemy

# creating the database instance
db = SQLAlchemy()

# creating the Flask app
app = Flask(__name__)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URL
db.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


