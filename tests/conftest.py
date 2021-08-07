from app import create_app, db
from config import TestingConfig
import pytest
from populate_db import init_db


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestingConfig).app

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    db.create_all()
    init_db(db)
    yield db

    db.drop_all()
