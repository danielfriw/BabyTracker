from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user

from main import db
from main.blueprints.events_blueprint.models import Event
from main.blueprints.events_blueprint.services import event_not_found_error_message, \
    get_event_activity_from_index_buttons, get_event_by_id

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
    comment = request.form['comment']
    new_event = Event(activity=activity,
                      user_id=current_user.id,
                      baby_name=session['baby_name'],
                      comment=comment)
    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('index'))



@events_blueprint.route('/update/<id>', methods=['GET'])
@login_required
def get_update_event(id):
    try:
        event = get_event_by_id(id)
        return render_template('update_event.html', event=event)
    except:
        flash(event_not_found_error_message())


@events_blueprint.route('/update/<id>', methods=['POST'])
@login_required
def post_update_event(id):
    try:
        event = get_event_by_id(id)
        new_comment = request.form['comment']
        event.comment = new_comment
        db.session.commit()
        return redirect(url_for('index'))
    except:
        flash(event_not_found_error_message())


@events_blueprint.route('/delete/<id>', methods=['GET'])
@login_required
def delete_event(id):
    try:
        event = get_event_by_id(id)
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        flash(event_not_found_error_message())
