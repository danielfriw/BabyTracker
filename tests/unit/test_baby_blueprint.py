import datetime
from unittest.mock import patch

import pytest
from flask import session, url_for

from extensions import db
from main.blueprints.baby_blueprint.models import Baby
from main.blueprints.baby_blueprint.services import set_baby_data_in_session, add_baby_to_db, \
    raise_error_if_invalid_baby_name, does_baby_name_already_exist_for_user, get_baby_by_id, get_baby_by_name


def test_get_add_baby(authenticated_client, app, captured_templates):
    with app.test_request_context():
        response = authenticated_client.get(url_for('baby.get_add_baby'), follow_redirects=True)

        assert response.status_code == 200
        assert len(captured_templates) == 1
        assert captured_templates[0][0].name == 'add_baby.html'


@patch('main.blueprints.baby_blueprint.views.BabyForm')
def test_post_add_baby_invalid_form(mock_baby_form, authenticated_client, app, captured_templates):
    mock_baby_form.return_value.validate_on_submit.return_value = False

    with app.test_request_context():
        response = authenticated_client.post(url_for('baby.post_add_baby'), follow_redirects=True)

        assert response.status_code == 200
        assert len(captured_templates) == 1
        assert captured_templates[0][0].name == 'add_baby.html'


@patch('main.blueprints.baby_blueprint.views.BabyForm')
@patch('main.blueprints.baby_blueprint.views.add_baby_to_db')
def test_post_add_baby_valid_form(mock_add_baby_to_db, mock_baby_form, authenticated_client, app, captured_templates):
    mock_baby_form.return_value.validate_on_submit.return_value = True
    mock_add_baby_to_db.return_value = None

    with app.test_request_context():
        response = authenticated_client.post(url_for('baby.post_add_baby'))

        assert response.status_code == 302
        mock_add_baby_to_db.assert_called_once()
        assert response.location == url_for('index.index')


@patch('main.blueprints.baby_blueprint.views.set_baby_data_in_session')
@patch('main.blueprints.baby_blueprint.views.get_baby_by_id')
def test_set_current_baby(mock_get_baby_by_id, mock_set_baby_data_in_session, app, authenticated_client):
    baby_id = 1
    mock_get_baby_by_id.return_value = True
    mock_set_baby_data_in_session.return_value = None

    with app.test_request_context():
        response = authenticated_client.get(url_for('baby.set_current_baby', baby_id=baby_id))

        assert response.status_code == 302
        mock_get_baby_by_id.assert_called_once_with(baby_id)
        mock_set_baby_data_in_session.assert_called_once()


@patch('main.blueprints.baby_blueprint.services.raise_error_if_invalid_baby_name')
@patch('main.blueprints.baby_blueprint.services.current_user')
@patch('main.blueprints.baby_blueprint.forms.BabyForm')
def test_add_baby_to_db(mock_baby_form, mock_current_user, mock_raise_error, app, client):
    """
    Test adding a baby to the database.
    :param mock_baby_form: mock of the BabyForm class
    :param mock_current_user: mock of the current_user object
    :param mock_raise_error: mock of the raise_error_if_invalid_baby_name function
    :param app: app fixture
    :param client: client fixture
    :return: - assert the DB holds only 1 baby
             - assert the baby with the name 'Mike' exists in the DB
             - assert the session holds the baby's name
    """
    mock_raise_error.return_value = None
    mock_current_user.id = 1

    mock_baby_form.name.data = 'Mike'
    mock_baby_form.gender.data = 'm'
    mock_baby_form.dob.data = datetime.date(2023, 11, 21)

    with app.test_request_context(), app.app_context():
        add_baby_to_db(mock_baby_form)

        assert Baby.query.count() == 1
        assert Baby.query.filter_by(name='Mike').first() is not None
        assert session['baby_name'] == 'Mike'


@pytest.mark.parametrize('invalid_name', ['123abc', 'Invalid Name', '', 'Invalid_name'])
def test_raise_error_if_invalid_baby_name(invalid_name, app):
    """
    Test raising an error if the baby's name is invalid.
    :param invalid_name: an invalid baby name
    :param app: app fixture
    :return: assert the ValueError message
    """
    with pytest.raises(ValueError) as excinfo:
        raise_error_if_invalid_baby_name(invalid_name)
    assert str(excinfo.value) == 'Invalid baby name, please use only alphabetic characters'


@patch('main.blueprints.baby_blueprint.services.does_baby_name_already_exist_for_user')
def test_raise_error_if_valid_baby_name_already_exists(mock_func, app):
    """
    Test raising an error if the baby's name already exists for a mocked return value.
    :param mock_func: mock of the does_baby_name_already_exist_for_user function
    :param app: app fixture
    :return: assert the ValueError message
    """
    mock_func.return_value = True

    with pytest.raises(ValueError) as excinfo:
        raise_error_if_invalid_baby_name('ValidName')

    assert str(excinfo.value) == 'You already have a baby with this name'


@patch('main.blueprints.baby_blueprint.services.current_user')
def test_does_baby_name_already_exist_for_user(mock_current_user, app):
    """
    Test checking if the baby's name already exists for the current user.
    :param mock_current_user:
    :param app:
    :return:
    """
    mock_current_user.id = 1

    with app.test_request_context():
        _ = create_baby_to_db('Alice')

        assert does_baby_name_already_exist_for_user('Alice')


def test_set_baby_data_in_session(app):
    """
    Test setting the baby data in the session.
    :param app: app fixture
    :return: - assert the session holds the baby's name
             - assert the session holds the baby's gender
             - assert the session holds the baby's id
    """
    with app.test_request_context():
        baby = create_baby_to_db('Tom')

        set_baby_data_in_session(baby)

        assert session['baby_name'] == 'Tom'
        assert session['baby_gender'] == 'm'
        assert session['baby_id'] == 1


@patch('main.blueprints.baby_blueprint.services.current_user')
def test_get_baby_by_id(mock_current_user, app):
    """
    Test the function for getting a baby by its id.
    :param mock_current_user: mock of the current_user object
    :param app: app fixture
    :return: assert the retrieved baby is the same as the created baby
    """
    mock_current_user.id = 1

    with app.test_request_context():
        baby = create_baby_to_db('Emily')
        retrieved_baby = get_baby_by_id(baby.id)

        assert retrieved_baby == baby

@patch('main.blueprints.baby_blueprint.services.current_user')
def test_get_baby_by_name(mock_current_user, app):
    """
    Test the function for getting a baby by its id.
    :param mock_current_user: mock of the current_user object
    :param app: app fixture
    :return: assert the retrieved baby is the same as the created baby
    """
    mock_current_user.id = 1

    with app.test_request_context():
        baby = create_baby_to_db('Sammy')
        retrieved_baby = get_baby_by_name(baby.name)

        assert retrieved_baby == baby


def create_baby_to_db(name):
    """
    Create a baby in the database and return it. Helper function for the tests.
    :return: Baby instance
    """
    baby = Baby(name=name, gender='m', dob=datetime.date(2024, 1, 1), user_id=1)
    db.session.add(baby)
    db.session.commit()
    return baby
