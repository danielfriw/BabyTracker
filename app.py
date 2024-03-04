from flask import render_template, redirect, url_for, session
from flask_login import login_required, current_user
from main.blueprints.baby_blueprint.baby_blueprint import baby_blueprint
from main.blueprints.auth_blueprint.auth_blueprint import auth_blueprint
from main.blueprints.events_blueprint.events_blueprint import events_blueprint
from main.blueprints.graphs_blueprint.graphs_blueprint import graphs_blueprint
from main.blueprints.api_baby_blueprint.api_baby_blueprint import api_baby_blueprint
from main import app, db
from main.blueprints.baby_blueprint.models import Baby
from main.blueprints.events_blueprint.models import Event
from main.utils.baby_context_processor_for_navbar_dropdown_list import baby_context_processor_for_navbar_dropdown_list

# Create tables (initialize the database)
with app.app_context():
    db.create_all()


# Context processors: these run before the template is rendered
# We use it here to render the users babies in the navbar dropdown list
app.context_processor(baby_context_processor_for_navbar_dropdown_list)


app.register_blueprint(baby_blueprint, url_prefix='/baby')
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(events_blueprint, url_prefix='/events')
app.register_blueprint(graphs_blueprint, url_prefix='/graphs')
app.register_blueprint(api_baby_blueprint, url_prefix='/api/baby')


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


if __name__ == '__main__':
    app.run(debug=True)
