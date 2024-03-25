from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

from extensions import db
from main.blueprints.events_blueprint.services import event_not_found_error_message, \
    get_event_by_id, create_new_event, update_event_data, get_event_activity_from_index_buttons

events_blueprint = Blueprint('events', __name__, url_prefix='/events', static_folder='static',
                             template_folder='templates')


@events_blueprint.route('/create_event', methods=['GET'])
@login_required
def get_create_event():
    activity = get_event_activity_from_index_buttons()
    return render_template('create_event.html', activity=activity)


@events_blueprint.route('/create_event', methods=['POST'])
@login_required
def post_create_event():
    activity = get_event_activity_from_index_buttons()
    create_new_event(activity)
    return redirect(url_for('index.index'))


@events_blueprint.route('/update/<id>', methods=['GET'])
@login_required
def get_update_event(id):
    try:
        event = get_event_by_id(id)
    except:
        flash(event_not_found_error_message())
    return render_template('update_event.html', event=event)


@events_blueprint.route('/update/<id>', methods=['POST'])
@login_required
def post_update_event(id):
    try:
        event = get_event_by_id(id)
        update_event_data(event)
    except:
        flash(event_not_found_error_message())
    return redirect(url_for('index.index'))


@events_blueprint.route('/delete_event/<id>', methods=['POST'])
@login_required
def delete_event(id):
    try:
        event = get_event_by_id(id)
        db.session.delete(event)
        db.session.commit()
    except:
        flash(event_not_found_error_message())
    return redirect(url_for('index.index'))
