import re

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp

from app.auth.models import User


class LoginForm(FlaskForm):
    email = StringField("Email: ",
                        validators=[DataRequired(),
                                    Length(10, 100),
                                    Email()],
                        render_kw={'placeholder': 'Enter email'})

    password = PasswordField("Password: ",
                             validators=[DataRequired()],
                             render_kw={'placeholder': 'Enter password'})

    remember = BooleanField("Check me out", default=False)
    submit = SubmitField("Log In",
                         render_kw={'class': 'btn btn-primary'})


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(1, 100),
                    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                    'Usernames must have only letters, numbers, underscores')],
        render_kw={'placeholder': 'Enter your name'})

    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 100), Email()],
                        render_kw={'placeholder': 'Enter email'})

    age = StringField("Age: ",
                      validators=[Length(min=1, max=3, message="Age must be between 1 and 3 characters")],
                      render_kw={'placeholder': 'Enter age'})

    city = StringField("City: ",
                       validators=[Length(min=2, max=100, message="City must be between 1 and 3 characters")],
                       render_kw={'placeholder': 'Enter city'})

    info = StringField('Info',
                       validators=[DataRequired(), Length(1, 100)],
                       render_kw={'placeholder': 'Enter information about yourself'})

    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('password_repeat', message='Passwords must match')])

    password_repeat = PasswordField('Confirm password',
                                    validators=[DataRequired()])

    submit = SubmitField('Register',
                         render_kw={'class': 'btn btn-primary'})

    def validate_username(self, username):
        if User.select().where(User.username == username.data).first():
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if User.select().where(User.email == email.data).first():
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_password(self, password):
        length_error = len(password.data) < 8
        digit_error = re.search(r"\d", password.data) is None
        uppercase_error = re.search(r"[A-Z]", password.data) is None
        lowercase_error = re.search(r"[a-z]", password.data) is None
        symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password.data) is None

        password_error = any([length_error, digit_error, uppercase_error, lowercase_error, symbol_error])

        if password_error:
            raise ValidationError('Password must be at least 8 chars include Upper, Lower, Digit, Punctuation')


class UpdateAccountForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(1, 100)],
        render_kw={'placeholder': 'Enter your name'})

    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 100), Email()],
                        render_kw={'placeholder': 'Enter email'})

    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update',
                         render_kw={'class': 'btn btn-primary'})

    def validate_username(self, username):
        if username.data != current_user.username:
            if User.select().where(User.username == username.data).first():
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.select().where(User.email == email.data).first():
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField("Email: ",
                        validators=[DataRequired(),
                                    Length(10, 100),
                                    Email()],
                        render_kw={'placeholder': 'Enter email'})

    submit = SubmitField("Request Password Reset",
                         render_kw={'class': 'btn btn-success'})

    def validate_email(self, email):
        user = User.select().where(User.email == email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('password_repeat', message='Passwords must match')],
                             render_kw={'placeholder': 'Enter password'})

    password_repeat = PasswordField('Confirm password',
                                    validators=[DataRequired()],
                                    render_kw={'placeholder': 'Repeat password'})

    submit = SubmitField('Reset Password',
                         render_kw={'class': 'btn btn-success'})