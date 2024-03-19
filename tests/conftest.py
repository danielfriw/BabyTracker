import pytest
from app import create_app


@pytest.fixture(scope='module')
def app():
    app= create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    yield app

# @pytest.fixture(scope='module')
# def db(app, db):
#     # db.app = app  # Bind the database to the created app
#     db.create_all()
#     yield db
#     db.drop_all()
#
# @pytest.fixture(scope='function')
# def session(db):
#     connection = db.engine.connect()
#     transaction = connection.begin()
#
#     options = dict(bind=connection, binds={})
#     session = db.create_scoped_session(options=options)
#
#     db.session = session
#
#     yield session
#
#     transaction.rollback()
#     connection.close()
#     session.remove()

@pytest.fixture(scope='function')
def client(app):
    """
    Create a test client for the app.
    """
    return app.test_client()