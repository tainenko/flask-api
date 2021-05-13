import pytest
from app import init_app
from database import db


@pytest.fixture
def app():
    return init_app('test')


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()
