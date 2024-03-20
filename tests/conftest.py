import pytest
from app import create_app


@pytest.fixture(scope='function')
def app():
    app= create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    yield app


@pytest.fixture(scope='function')
def client(app):
    """
    Create a test client for the app.
    """
    return app.test_client()