import datetime
from unittest.mock import patch

import pytest
from flask import session
from flask_login import current_user

from extensions import db
from main.blueprints.baby_blueprint.models import Baby
from main.blueprints.baby_blueprint.services import set_baby_data_in_session, add_baby_to_db, \
    raise_error_if_invalid_baby_name, does_baby_name_already_exist_for_user


def test_request_example(client):
    response = client.get("/baby/add_baby")
    assert response.status_code == 302


def test_set_baby_data_in_session(app):

    with app.test_request_context():
        baby = Baby(name='Tom', gender='m', dob=datetime.date(2024, 1, 1), user_id=1)
        db.session.add(baby)
        db.session.commit()

        set_baby_data_in_session(baby)

        assert session['baby_name'] == 'Tom'
        assert session['baby_gender'] == 'm'
        assert session['baby_id'] == 1


@patch('main.blueprints.baby_blueprint.services.raise_error_if_invalid_baby_name')
@patch('main.blueprints.baby_blueprint.services.current_user')
@patch('main.blueprints.baby_blueprint.forms.BabyForm')
def test_add_baby_to_db(mock_baby_form, mock_current_user, mock_raise_error, app, client):

    mock_raise_error.return_value = None
    mock_current_user.id = 1

    mock_baby_form.name.data = 'Mike'.capitalize()  # Directly capitalize the string here
    mock_baby_form.gender.data = 'm'
    mock_baby_form.dob.data = datetime.date(2023, 11, 21)

    with app.test_request_context():  # Allow access to session
        with app.app_context():  # Allow access to the database
            add_baby_to_db(mock_baby_form)

            assert Baby.query.count() == 1
            assert Baby.query.filter_by(name='Mike').first() is not None
            assert session['baby_name'] == 'Mike'

@pytest.mark.parametrize('invalid_name', ['123abc', 'Invalid Name', '', 'Invalid_name'])
def test_raise_error_if_invalid_baby_name(invalid_name, app):

    with pytest.raises(ValueError) as excinfo:
        raise_error_if_invalid_baby_name(invalid_name)
    assert str(excinfo.value) == 'Invalid baby name, please use only alphabetic characters'

@patch('main.blueprints.baby_blueprint.services.does_baby_name_already_exist_for_user')
def test_raise_error_if_valid_baby_name_already_exists(mock_func, app):

    mock_func.return_value = True

    with pytest.raises(ValueError) as excinfo:
        raise_error_if_invalid_baby_name('ValidName')

    assert str(excinfo.value) == 'You already have a baby with this name'

@patch('main.blueprints.baby_blueprint.services.current_user')
def test_does_baby_name_already_exist_for_user(mock_current_user, app):

    mock_current_user.id = 1

    with app.test_request_context():
        baby = Baby(name='Alice', gender='m', dob=datetime.date(2024, 1, 1), user_id=1)
        db.session.add(baby)
        db.session.commit()

        assert does_baby_name_already_exist_for_user('Alice')

# def test_does_baby_name_already_exist_for_user(app, create_baby):
#     baby1 = create_baby('Bob')
#     assert does_baby_name_already_exist_for_user('Bob')  # True for existing name
#     assert not does_baby_name_already_exist_for_user('Charlie')  # False for non-existing name
#
# def test_get_baby_by_id(app, create_baby):
#     baby = create_baby('Emily')
#     retrieved_baby = get_baby_by_id(baby.id)
#     assert retrieved_baby == baby
#
# def test_get_baby_by_id_not_found(app):
#     assert get_baby_by_id(999) is None  # Check for non-existent baby
