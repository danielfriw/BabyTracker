from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import login_required, current_user
from main.blueprints.baby_blueprint.forms import BabyForm
from main.blueprints.baby_blueprint.models import Baby, db

baby_blueprint = Blueprint('baby', __name__, url_prefix='/baby', static_folder='static', template_folder='templates')


@baby_blueprint.route('/add_baby', methods=['GET', 'POST'])
@login_required
def add_baby():
    """
    Add a baby for the current user.
    :return: a redirect to the index page after adding the baby
    """
    form = BabyForm()
    if form.validate_on_submit():

        try:
            add_baby_to_db(form)
            add_baby_to_session(form)

        except ValueError as ve:
            flash(str(ve))
            return redirect(url_for('baby.add_baby'))

        return redirect(url_for('index'))
    return render_template('add_baby.html', form=form)


def add_baby_to_db(form):
    """
    Add a baby to the database.
    :param form: the form with the baby's information posted from the web page
    """
    baby = Baby(name=form.name.data.capitalize(), gender=form.gender.data, dob=form.dob.data, user_id=current_user.id)
    raise_error_if_baby_name_exists(baby)
    db.session.add(baby)
    db.session.commit()


def raise_error_if_baby_name_exists(baby):
    """
    Raise an error if the baby's name already exists for the current user.
    :param baby: the baby
    """
    existing_baby = Baby.query.filter_by(user_id=current_user.id, name=baby.name).first()
    if existing_baby and baby.name == existing_baby.name:
        raise ValueError('You already have a baby with this name')


def add_baby_to_session(form):
    """
    Add the baby information to the session, allowing for smooth transition between the web pages.
    :param form: the form with the baby's information posted from the web page
    """
    baby = Baby.query.filter_by(user_id=current_user.id, name=form.name.data.capitalize()).first()
    session['baby_name'] = baby.name
    session["baby_gender"] = baby.gender
    session['baby_id'] = baby.id


@baby_blueprint.route('/set_current_baby/<int:baby_id>')
@login_required
def set_current_baby(baby_id):
    """
    Set the current baby in the session, this is used by the navbar to display the current baby.
    :param baby_id: the baby's id we want to set as the current baby
    :return: redirect (refresh) the current page we are working from
    """
    baby = Baby.query.filter_by(id=baby_id, user_id=current_user.id).first()
    if baby:
        session["baby_name"] = baby.name
        session["baby_gender"] = baby.gender
        session["baby_id"] = baby.id
    return redirect(request.referrer)
