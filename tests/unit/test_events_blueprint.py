import datetime
from unittest.mock import patch, MagicMock

import pytest
from flask import session, url_for

from extensions import db
from main.blueprints.events_blueprint.models import Event
from main.blueprints.events_blueprint.services import event_not_found_error_message, \
     get_event_by_id, create_new_event, update_event_data, get_event_activity_from_index_buttons
from main.blueprints.events_blueprint.views import delete_event


@patch('main.blueprints.events_blueprint.views.get_event_activity_from_index_buttons')
def test_get_create_event(mock_get_event_activity, authenticated_client, app, captured_templates):
    mock_get_event_activity.return_value = 'Feeding'

    with app.test_request_context():
        response = authenticated_client.get(url_for('events.get_create_event'))

        assert response.status_code == 200
        assert len(captured_templates) == 1
        assert captured_templates[0][0].name == 'create_event.html'


@patch('main.blueprints.events_blueprint.views.create_new_event')
@patch('main.blueprints.events_blueprint.views.get_event_activity_from_index_buttons')
def test_post_create_event(mock_get_event_activity, mock_create_new_event, authenticated_client, app):
    mock_get_event_activity.return_value = 'Feeding'
    mock_create_new_event.return_value = None

    response = authenticated_client.post(url_for('events.post_create_event'))

    assert response.status_code == 302
    mock_create_new_event.assert_called_once()
    assert response.location == url_for('index.index')


@patch('main.blueprints.events_blueprint.views.get_event_by_id')
def test_get_update_event(mock_get_event_by_id, authenticated_client, app, captured_templates):
    event = Event(activity='Feeding', user_id=1, baby_name='Mike', comment='Old comment')
    db.session.add(event)
    db.session.commit()
    mock_get_event_by_id.return_value = event

    with app.test_request_context():
        response = authenticated_client.get(url_for('events.get_update_event', id=1))

        assert response.status_code == 200
        assert len(captured_templates) == 1
        assert captured_templates[0][0].name == 'update_event.html'


@patch('main.blueprints.events_blueprint.views.get_event_by_id')
@patch('main.blueprints.events_blueprint.views.update_event_data')
def test_post_update_event(mock_update_event_data, mock_get_event_by_id, authenticated_client, app, captured_templates):
    event = Event(activity='Feeding', user_id=1, baby_name='Mike', comment='Old comment')
    db.session.add(event)
    db.session.commit()
    mock_get_event_by_id.return_value = event
    mock_update_event_data.return_value = None

    with app.test_request_context():
        response = authenticated_client.post(url_for('events.post_update_event', id=1))

        assert response.status_code == 302
        mock_update_event_data.assert_called_once()
        assert response.location == url_for('index.index')


@patch('main.blueprints.events_blueprint.views.get_event_by_id')
def test_delete_event(mock_get_event_by_id, authenticated_client, app):

    with app.test_request_context():
        event = Event(activity='Feeding', user_id=1, baby_name='Mike', comment='Comment')
        db.session.add(event)
        db.session.commit()
        mock_get_event_by_id.return_value = event

        response = authenticated_client.post(url_for('events.delete_event', id=1))

        assert response.status_code == 302
        assert Event.query.count() == 0
        assert response.location == url_for('index.index')


def test_event_not_found_error_message():
    """
    Test that the correct error message is returned when an event is not found.
    """
    message = event_not_found_error_message()
    assert message == "Event not found."

@patch('main.blueprints.events_blueprint.services.get_data_from_html_form')
@patch('main.blueprints.events_blueprint.services.current_user')
def test_create_new_event(mock_current_user,mock_get_comment_from_html_form, authenticated_client, app):
    """
    Test creating a new event and adding it to the database.
    """

    with app.test_request_context():
        activity = 'Feeding'
        mock_get_comment_from_html_form.return_value = 'Test comment'
        mock_current_user.id = 1
        session['baby_name'] = 'Mike'

        create_new_event(activity)

        assert Event.query.count() == 1
        event = Event.query.first()
        assert event.activity == 'Feeding'
        assert event.user_id == 1
        assert event.baby_name == 'Mike'
        assert event.comment == 'Test comment'

@patch('main.blueprints.events_blueprint.services.get_data_from_html_form')
def test_update_event_data(mock_get_comment_from_html_form, app):
    """
    Test updating an event's comment.
    """
    with app.test_request_context():
        mock_get_comment_from_html_form.return_value = 'New comment'

        event = Event(activity='Feeding', user_id=1, baby_name='Mike', comment='Old comment')
        db.session.add(event)
        db.session.commit()

        update_event_data(event)

        assert event.comment == 'New comment'

def test_get_event_by_id(app):
    """
    Test getting an event by its id.
    """
    with app.test_request_context():
        event = Event(activity='Feeding', user_id=1, baby_name='Mike', comment='Comment')
        db.session.add(event)
        db.session.commit()

        event = get_event_by_id(1)

        assert event.activity == 'Feeding'
        assert event.user_id == 1
        assert event.baby_name == 'Mike'
        assert event.comment == 'Comment'