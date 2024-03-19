import datetime
from unittest.mock import patch
from flask import session
from flask_login import current_user

from extensions import db
from main.blueprints.baby_blueprint.models import Baby
from main.blueprints.baby_blueprint.services import set_baby_data_in_session


def test_request_example(client):
    response = client.get("/baby/add_baby")
    assert response.status_code == 302


def test_set_baby_data_in_session(app):
    baby = Baby(name='test', gender='m', dob=datetime.date(2024,1,1), user_id=1)
    with app.test_request_context():
        db.session.add(baby)
        db.session.commit()

        set_baby_data_in_session(baby)

        assert session['baby_name'] == 'test'
        assert session['baby_gender'] == 'm'
        assert session['baby_id'] == 1
#
# @patch('main.blueprints.baby_blueprint.services.BabyForm')
# def test_add_baby_to_db(app, client, login_user, create_baby, mock_form):
#
#     mock_form.name.data = 'Alice'
#     mock_form.gender.data = 'female'
#     mock_form.dob.data = '2023-11-21'
#
#     response = client.post('/add_baby', data=mock_form.data)  # Assuming route for create action
#
#     assert response.status_code == 302  # Assuming redirect on success
#     assert Baby.query.filter_by(name='Alice').first() is not None
#     assert 'baby_name' in session  # Check session data set
#
# @pytest.mark.parametrize('invalid_name', ['123abc', 'John Doe', '', '!@#'])
# def test_raise_error_if_invalid_baby_name(invalid_name):
#     with pytest.raises(ValueError) as excinfo:
#         raise_error_if_invalid_baby_name(invalid_name)
#     assert str(excinfo.value) == 'Invalid baby name, please use only alphabetic characters'
#
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