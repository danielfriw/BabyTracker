import datetime
from unittest.mock import patch

import pytest
from flask import session, url_for

from extensions import db
from main.blueprints.events_blueprint.models import Event
from main.blueprints.events_blueprint.services import event_not_found_error_message, \
    get_event_activity_from_index_buttons, get_event_by_id


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


@patch('main.blueprints.events_blueprint.services.get_event_by_id')
def test_get_update_event(mock_get_event_by_id, authenticated_client, app, captured_templates):
    mock_event = Event(id=1, activity='Feeding', user_id=1, baby_name='Mike', comment='Old comment')
    mock_get_event_by_id.return_value = mock_event

    with app.test_request_context():
        response = authenticated_client.get(url_for('events.get_update_event', id=1), follow_redirects=True)

        assert response.status_code == 200
        assert len(captured_templates) == 1
        assert captured_templates[0][0].name == 'update_event.html'


@patch('main.blueprints.events_blueprint.services.get_event_by_id')
def test_post_update_event(mock_get_event_by_id, authenticated_client, app, captured_templates):
    mock_event = Event(id=1, activity='Feeding', user_id=1, baby_name='Mike', comment='Old comment')
    mock_get_event_by_id.return_value = mock_event

    with app.test_request_context(), app.app_context():
        response = authenticated_client.post(url_for('events.post_update_event', id=1), data={
            'comment': 'Updated comment'
        }, follow_redirects=True)

        assert response.status_code == 302
        updated_event = Event.query.get(1)
        assert updated_event.comment == 'Updated comment'


@patch('main.blueprints.events_blueprint.services.get_event_by_id')
def test_delete_event(mock_get_event_by_id, authenticated_client, app):
    mock_event = Event(id=1, activity='Feeding', user_id=1, baby_name='Mike', comment='Comment')
    mock_get_event_by_id.return_value = mock_event

    with app.test_request_context(), app.app_context():
        response = authenticated_client.get(url_for('events.delete_event', id=1), follow_redirects=True)

        assert response.status_code == 302
        assert Event.query.count() == 0


def test_event_not_found_error_message():
    """
    Test that the correct error message is returned when an event is not found.
    """
    message = event_not_found_error_message()
    assert message == "Event not found."
