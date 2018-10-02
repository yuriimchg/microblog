# FlaskForm is responsible for simple performing of forms
from flask_wtf import FlaskForm
# wtforms contains form templates
from wtforms import StringField, PasswordField, BooleanField, SubmitField
# validators prevent from submitting empty forms
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    # User and password fields are required
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    # Remember me check
    remember_me = BooleanField('Remember Me')
    # Submit button
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    #
    val_password = StringField('Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("This username is already used. Please, choose another one")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("This e-mail is already used. Please, choose another one")
