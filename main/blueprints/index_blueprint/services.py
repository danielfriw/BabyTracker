from flask import render_template, session
from flask_login import current_user

from main.blueprints.baby_blueprint.models import Baby
from main.blueprints.events_blueprint.models import Event


def is_a_baby_assigned_to_session():
    return session.get('baby_name') is not None


def does_user_have_babies():
    """
    Check if the user has babies.
    :return: True if the user has babies, False otherwise.
    """
    babies = Baby.query.filter_by(user_id=current_user.id).all()
    return len(babies) > 0


def render_index_page_with_all_events():
    events = (Event.query.filter_by(user_id=current_user.id,
                                    baby_name=session['baby_name'])
              .order_by(Event.created_at.desc())
              .all())
    return render_template('index.html', events=events)
