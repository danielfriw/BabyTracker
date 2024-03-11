from flask import session
from flask_login import current_user

from main.blueprints.baby_blueprint.models import Baby, db


def set_baby_data_in_session(baby):
    """
    Add the baby information to the session, allowing for smooth transition between the web pages.
    :param baby: Baby instance to be added to the session
    """
    session['baby_name'] = baby.name
    session['baby_gender'] = baby.gender
    session['baby_id'] = baby.id


def add_baby_to_db(form):
    """
    Create a Baby instance from the form data, add it to the database, and set its data in the session.
    :param form: BabyForm instance containing the submitted data
    """
    baby_data = {
        'name': form.name.data.capitalize(),
        'gender': form.gender.data,
        'dob': form.dob.data,
        'user_id': current_user.id
    }

    raise_error_if_invalid_baby_name(baby_data['name'])

    baby = Baby(**baby_data)
    db.session.add(baby)
    db.session.commit()

    set_baby_data_in_session(baby)


def raise_error_if_invalid_baby_name(baby_name):
    """
    Check if a baby's name contains only alphabetic characters.
    :param name: the baby's name to be validated
    :return: True if the name is valid, False otherwise
    """
    if not baby_name.isalpha():
        raise ValueError('Invalid baby name, please use only alphabetic characters')
    if does_baby_name_already_exist_for_user(baby_name):
        raise ValueError('You already have a baby with this name')


def does_baby_name_already_exist_for_user(baby_name):
    """
    Raise an error if the baby's name already exists for the current user.
    :param baby: Baby instance
    """
    return baby_name == Baby.query.filter_by(user_id=current_user.id, name=baby_name).first()


def get_baby_by_id(baby_id):
    """
    Retrieve a baby by ID for the current user.
    :param baby_id: The baby's ID
    :return: Baby instance or None if not found
    """
    return Baby.query.filter_by(id=baby_id, user_id=current_user.id).first()
