from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    # registration form using flask forms and validators
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign-Up')

    # def validate_field(self, field):
    #     # custom validation check template
    #     if true:
    #         raise ValidationError("Validation Message")

    def validate_username(self, username):
        # custom validation check to see if username already exists
        user = User.query.filter_by(username=username.data).first()  # if user doesn't exist, returns none
        if user:
            raise ValidationError("Username already in use. Please choose another one.")

    def validate_email(self, email):
        # custom validation check to see if email already exists
        user = User.query.filter_by(email=email.data).first()  # if email doesn't exist, returns none
        if user:
            raise ValidationError("Email already in use. Please choose another one.")


class LoginForm(FlaskForm):
    # login form using flask forms and validators
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    # registration form using flask forms and validators
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        # custom validation check to see if username already exists
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()  # if user doesn't exist, returns none
            if user:
                raise ValidationError("Username already in use. Please choose another one.")

    def validate_email(self, email):
        # custom validation check to see if email already exists
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()  # if email doesn't exist, returns none
            if user:
                raise ValidationError("Email already in use. Please choose another one.")


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
