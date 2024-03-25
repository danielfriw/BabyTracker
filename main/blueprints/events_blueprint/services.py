from flask import request, session
from flask_login import current_user

from extensions import db
from main.blueprints.events_blueprint.models import Event
from main.utils.utils import get_data_from_html_form


def event_not_found_error_message():
    """
    Return an error message when an event is not found.
    :return: str
    """
    return "Event not found."


def get_event_activity_from_index_buttons():
    """
    Get the activity from the index buttons (homepage).
    :return: activity
    """
    return request.args.get('activity')


def create_new_event(activity):
    """
    Create a new event and add it to the database.
    :param activity: the activity of the event
    """
    comment = get_data_from_html_form('comment')
    new_event = Event(activity=activity,
                      user_id=current_user.id,
                      baby_name=session['baby_name'],
                      comment=comment)
    db.session.add(new_event)
    db.session.commit()
    pass


def update_event_data(event):
    """
    Update an event's comment.
    :param event: event instance
    :param new_comment: str
    """
    new_comment = get_data_from_html_form('comment')
    event.comment = new_comment
    db.session.commit()
    pass


def get_event_by_id(id):
    """
    Get an event by its id.
    :param id: event's id
    :return: event instance
    """
    event = Event.query.get_or_404(ident=id)
    return event
