from contextlib import contextmanager

import pytest
from flask import template_rendered, session
from flask_login import login_user, logout_user

from app import create_app
from extensions import db
from main.blueprints.auth_blueprint.models import User


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

@pytest.fixture(scope='function')
def user(app):
    with app.app_context():
        user = User(username='testuser', email='test@example.com', password='testpass')
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()

@pytest.fixture
def authenticated_client(client, user, app):
    with app.app_context(), app.test_request_context():
        login_user(user)
        yield client

        logout_user()

@pytest.fixture(scope='function')
def captured_templates(app):
    """
    Capture templates rendered during a request.
    This was taken from the Flask documentation.
    :return: a list of tuples of the templates and contexts
    """
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
        recorded.clear()


