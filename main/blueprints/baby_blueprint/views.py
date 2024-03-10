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
            create_and_add_baby(form)
        except ValueError as ve:
            flash(str(ve))
            return redirect(url_for('baby.add_baby'))

        return redirect(url_for('index'))

    return render_template('add_baby.html', form=form)

def create_and_add_baby(form):
    """
    Create a Baby instance from the form data, add it to the database, and set its data in the session.
    :param form: BabyForm instance containing the submitted data
    """
    baby_data = {
        'name': form.name.data.capitalize(),
        'gender': form.gender.data,
        'dob': form.dob.data,
        'user_id': current_user.id
    }

    baby = create_baby_instance(baby_data)
    add_baby_to_db(baby)
    set_baby_data_in_session(baby)

def create_baby_instance(baby_data):
    """
    Create a Baby instance from the provided data.
    :param baby_data: Dictionary containing baby information
    :return: Baby instance
    """
    return Baby(**baby_data)

def add_baby_to_db(baby):
    """
    Add a baby to the database.
    :param baby: Baby instance to be added to the database
    """
    raise_error_if_baby_name_exists(baby)
    raise_error_if_invalid_baby_name(baby.name)
    db.session.add(baby)
    db.session.commit()

def raise_error_if_baby_name_exists(baby):
    """
    Raise an error if the baby's name already exists for the current user.
    :param baby: Baby instance
    """
    existing_baby = Baby.query.filter_by(user_id=current_user.id, name=baby.name).first()
    if existing_baby and baby.name == existing_baby.name:
        raise ValueError('You already have a baby with this name')

def raise_error_if_invalid_baby_name(name):
    """
    Check if a baby's name contains only alphabetic characters.
    :param name: the baby's name to be validated
    :return: True if the name is valid, False otherwise
    """
    if not name.isalpha():
        raise ValueError('Invalid baby name, please use only alphabetic characters')

def set_baby_data_in_session(baby):
    """
    Add the baby information to the session, allowing for smooth transition between the web pages.
    :param baby: Baby instance to be added to the session
    """
    session['baby_name'] = baby.name
    session['baby_gender'] = baby.gender
    session['baby_id'] = baby.id

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

def get_baby_by_id(baby_id):
    """
    Retrieve a baby by ID for the current user.
    :param baby_id: The baby's ID
    :return: Baby instance or None if not found
    """
    return Baby.query.filter_by(id=baby_id, user_id=current_user.id).first()
