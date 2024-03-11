from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user

from main import db
from main.blueprints.events_blueprint.models import Event

def event_not_found_error_message():
    return "Event not found."

def get_event_activity_from_index_buttons():
    activity = request.args.get('activity')
    return activity

def get_event_by_id(id):
    event = Event.query.get_or_404(ident=id)
    return event