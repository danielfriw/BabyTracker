from flask import request

from main.blueprints.events_blueprint.models import Event


def event_not_found_error_message():
    return "Event not found."

def get_event_activity_from_index_buttons():
    activity = request.args.get('activity')
    return activity

def get_event_by_id(id):
    event = Event.query.get_or_404(ident=id)
    return event