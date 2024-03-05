from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from main import db
from main.blueprints.events_blueprint.models import Event

events_blueprint = Blueprint('events', __name__, url_prefix='/events', static_folder='static',
                             template_folder='templates')


# create event:
@events_blueprint.route('/create_event', methods=['POST'])
@login_required
def create_event():
    activity = request.form['activity']
    return redirect(url_for('events.event_comments', activity=activity))


# event comments:
@events_blueprint.route('/event_comments', methods=['POST', 'GET'])
@login_required
def event_comments():
    activity = request.args.get('activity')
    if request.method == 'POST':
        comment = request.form['comment']
        new_event = Event(activity=activity, user_id=current_user.id, baby_name=session['baby_name'], comment=comment)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('event_comments.html', activity=activity)


# update event comment by id:
@events_blueprint.route('/update/<id>', methods=['POST', 'GET'])
@login_required
def update_event(id):
    event = Event.query.get_or_404(ident=id)
    if request.method == 'POST':
        new_comment = request.form['comment']
        event.comment = new_comment
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_event.html', event=event)


# delete event by id:
@events_blueprint.route('/delete/<id>', methods=['GET'])
@login_required
def delete_event(id):
    event = Event.query.get_or_404(ident=id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('index'))
