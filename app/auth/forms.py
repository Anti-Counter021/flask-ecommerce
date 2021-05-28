from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField
)

from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
    Length
)

from app.models import User


class LoginForm(FlaskForm):
    """ Login """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    """ Registration """
