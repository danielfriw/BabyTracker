from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from main.blueprints.baby_blueprint.forms import BabyForm
from main.blueprints.baby_blueprint.services import add_baby_to_db, set_baby_data_in_session, get_baby_by_id

baby_blueprint = Blueprint('baby', __name__, url_prefix='/baby', static_folder='static', template_folder='templates')


@baby_blueprint.route('/add_baby', methods=['GET'])
@login_required
def get_add_baby():
    """
    Add a baby for the current user.
    :return: a redirect to the index page after adding the baby
    """
    form = BabyForm()
    return render_template('add_baby.html', form=form)


@baby_blueprint.route('/add_baby', methods=['POST'])
@login_required
def post_add_baby():
    """
    Add a baby for the current user.
    :return: a redirect to the index page after adding the baby
    """
    form = BabyForm()

    if not form.validate_on_submit():
        return render_template('add_baby.html', form=form)

    try:
        add_baby_to_db(form)
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('baby.get_add_baby'))

    return redirect(url_for('index'))




@baby_blueprint.route('/set_current_baby/<int:baby_id>')
@login_required
def set_current_baby(baby_id):
    """
    Set the current baby in the session, used by the navbar to display the current baby.
    :param baby_id: The baby's id to set as the current baby
    :return: Redirect (refresh) the current page
    """
    baby = get_baby_by_id(baby_id)
    if baby:
        set_baby_data_in_session(baby)
    return redirect(request.referrer)
