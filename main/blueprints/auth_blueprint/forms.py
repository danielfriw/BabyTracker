from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from main.blueprints.auth_blueprint.models import User


class BaseForm(FlaskForm):

    def __init__(self, form=None, **kwargs):
        super().__init__(form=form, **kwargs)

    def check_form_validators_passed(self, form):
        if not form.validate_on_submit():
            error_messages = '\n '.join(error[0] for error in form.errors.values())
            raise ValidationError(error_messages)

    def check_if_email_exists(self, email):
        if User.query.filter_by(email=email.data).first():
            return True
        return False


class LoginForm(BaseForm):

    def __init__(self, form=None, **kwargs):
        super().__init__(form=form, **kwargs)

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

    def check_if_user_does_not_exists(self, email):
        if not self.check_if_email_exists(email):
            raise ValidationError('User does not exist')

    def check_if_password_is_not_correct(self, email, password):
        user = User.query.filter_by(email=email.data).first()
        if not user.check_password(password.data):
            raise ValidationError('Password incorrect')


class RegistrationForm(BaseForm):

    def __init__(self, form=None, **kwargs):
        super().__init__(form=form, **kwargs)

    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_if_email_already_exists(self, email):
        if self.check_if_email_exists(email):
            raise ValidationError('Email already registered')

    def check_if_username_already_exists(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already registered')
