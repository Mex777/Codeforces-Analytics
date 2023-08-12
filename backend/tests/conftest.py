import pytest
from flask import Flask

from backend.app.config import DATABASE_CONNECTION_URL
from backend.app.extensions import db
from backend.app.app import create_app


@pytest.fixture()
def app():
    app = create_app("sqlite://")

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    # with app.test_client() as client:
    #     return client
    return app.test_client()
