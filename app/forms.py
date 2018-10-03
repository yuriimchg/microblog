# FlaskForm is responsible for simple performing of forms
from flask_wtf import FlaskForm
# wtforms contains form templates
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
# validators prevent from submitting empty forms
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length
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
    # Second password field to validate the password
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

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=640)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        # Super function takes the current username as argument
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            # Rename username
            user = User.query.filter_by(username=self.username.data).first()
        # Print the error message if the name of existing user is chosen
            if user is not None:
                raise ValidationError("Please, pick another username.")

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
