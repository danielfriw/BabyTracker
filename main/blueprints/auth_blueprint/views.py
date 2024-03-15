from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from wtforms import ValidationError

from main.blueprints.auth_blueprint.forms import LoginForm, RegistrationForm
from main.blueprints.auth_blueprint.services import get_user_from_db_by_email, \
    check_registration_form_submission_is_valid, \
    check_login_form_submission_is_valid, add_user_to_db, remove_baby_data_from_session

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth', static_folder='static', template_folder='templates')


@auth_blueprint.route('/login', methods=['GET'])
def get_login():
    """
    Display the login form.
    :return: render the login page
    """
    form = LoginForm()
    return render_template('login.html', form=form)


@auth_blueprint.route('/login', methods=['POST'])
def post_login():
    """
    Log in the user if the form submission is valid.
    :return: redirect to the index page if the login is successful, otherwise redirect to the login page.
    """
    form = LoginForm()
    try:
        check_login_form_submission_is_valid(form)
        login_user(get_user_from_db_by_email(email=form.email.data))
    except ValueError as ve:
        flash(str(ve))
        return redirect(url_for('auth.get_login'))
    return redirect(url_for('index'))


@auth_blueprint.route('/register', methods=['GET'])
def get_register():
    """
    Display the registration form.
    :return: render the registration page
    """
    form = RegistrationForm()
    return render_template('register.html', form=form)


@auth_blueprint.route('/register', methods=['POST'])
def post_register():
    """
    Register the user if the form submission is valid.
    :return: redirect to the login page if the registration is successful, otherwise redirect to the registration page.
    """
    form = RegistrationForm(request.form)

    try:
        check_registration_form_submission_is_valid(form)
        add_user_to_db(form)
    except ValidationError as ve:
        flash(str(ve))
        return redirect(url_for('auth.get_register'))

    flash('You have successfully registered')
    return redirect(url_for('auth.get_login'))


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    remove_baby_data_from_session()
    flash('You have been logged out')
    return redirect(url_for('index'))

