from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from main import db
from main.blueprints.auth_blueprint.forms import LoginForm, RegistrationForm
from main.blueprints.auth_blueprint.models import User
from main.blueprints.baby_blueprint.models import Baby



auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth', static_folder='static', template_folder='templates')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        baby = Baby.query.filter_by(user_id=user.id).first()

        if user:
            if user.check_password(form.password.data) and user is not None:
                login_user(user)

                if not baby:
                    return redirect(url_for('baby.add_baby'))

                return redirect(url_for('index'))

            else:
                flash('Password incorrect')
                return redirect(url_for('auth.login'))

    return render_template('login.html', form=form)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('baby_name', None)
    session.pop('baby_gender', None)
    session.pop('baby_id', None)
    flash('You have been logged out')
    return redirect(url_for('index'))