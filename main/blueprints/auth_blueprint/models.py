from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from main import db
from main import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.INTEGER, primary_key=True)
    email = db.Column(db.TEXT, nullable=False, index=True, unique=True)
    username = db.Column(db.TEXT, nullable=False, index=True, unique=True)
    password_hash = db.Column(db.TEXT, nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'Username: {self.username}, email: {self.email}'
