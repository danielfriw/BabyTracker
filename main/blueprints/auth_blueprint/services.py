from flask import session

from main import db
from main.blueprints.auth_blueprint.models import User
from main.blueprints.baby_blueprint.models import Baby


def get_user_from_db_by_email(email):
    return User.query.filter_by(email=email).first()


def check_login_form_submission_is_valid(form):
    """
    Check if the form submission is valid, for the login form.
    :param form: form instance containing the submitted data
    :return: None
    """
    form.check_form_validators_passed(form)
    form.check_if_user_does_not_exists(form.email)
    form.check_if_password_is_not_correct(form.email, form.password)
    pass


def check_registration_form_submission_is_valid(form):
    """
    Check if the form submission is valid, for the registration form.
    :param form: form instance containing the submitted data
    :return: None
    """
    form.check_form_validators_passed(form)
    form.check_if_email_already_exists(form.email)
    form.check_if_username_already_exists(form.username)
    pass


def check_if_user_has_baby(user_id):
    """
    Check if the user has a baby.
    :param user_id: user's id
    :return: True if the user has a baby, False otherwise
    """
    if Baby.query.filter_by(user_id=user_id).first():
        return True
    return False


def add_user_to_db(form):
    """
    Add the user to the database.
    :param form: form instance containing the submitted data
    :return: None
    """
    user = User(email=form.email.data, username=form.username.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    pass


def remove_baby_data_from_session():
    """
    Remove the baby information from the session.
    """
    session.pop('baby_name', None)
    session.pop('baby_gender', None)
    session.pop('baby_id', None)
