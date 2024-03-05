from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import login_required, current_user
from main.blueprints.baby_blueprint.forms import BabyForm
from main.blueprints.baby_blueprint.models import Baby, db

baby_blueprint = Blueprint('baby', __name__, url_prefix='/baby', static_folder='static', template_folder='templates')

@baby_blueprint.route('/add_baby', methods=['GET', 'POST'])
@login_required
def add_baby():
    session['baby'] = None
    form = BabyForm()
    if form.validate_on_submit():
        baby = Baby(name=form.name.data.capitalize(), gender=form.gender.data, dob=form.dob.data,
                    user_id=current_user.id)
        existing_baby = Baby.query.filter_by(user_id=current_user.id, name=baby.name).first()

        if existing_baby and baby.name == existing_baby.name:
            flash('You already have a baby with this name')
            return redirect(url_for('baby.add_baby'))

        db.session.add(baby)
        db.session.commit()

        session['baby_name'] = baby.name
        session["baby_gender"] = baby.gender
        session['baby_id'] = baby.id

        return redirect(url_for('index'))
    return render_template('add_baby.html', form=form)


@baby_blueprint.route('/set_current_baby/<int:baby_id>')
@login_required
def set_current_baby(baby_id):
    baby = Baby.query.filter_by(id=baby_id, user_id=current_user.id).first()
    if baby:
        session["baby_name"] = baby.name
        session["baby_gender"] = baby.gender
        session["baby_id"] = baby.id
    return redirect(request.referrer)