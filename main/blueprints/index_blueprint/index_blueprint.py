from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_required, current_user
from main import app
from main.blueprints.events_blueprint.models import Event
from main.blueprints.baby_blueprint.models import Baby

index_blueprint = Blueprint('index', __name__, url_prefix='/', static_folder='static', template_folder='templates',
                            static_url_path='/main/blueprints/index_blueprint/static')


@app.route('/')
@login_required
def index():
    if session.get('baby_name') is None:
        babies = Baby.query.filter_by(user_id=current_user.id).all()
        if len(babies) > 0:
            session['baby_name'] = babies[0].name
            session["baby_gender"] = babies[0].gender
            session['baby_id'] = babies[0].id
        else:
            return redirect(url_for('baby.add_baby'))

    user_id = current_user.id
    events = Event.query.filter_by(user_id=user_id).filter_by(baby_name=session['baby_name']).order_by(
        Event.created_at.desc()).all()
    return render_template('index.html', events=events)
