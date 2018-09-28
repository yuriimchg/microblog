# FlaskForm is responsible for simple performing of forms
from flask_wtf import FlaskForm
# wtforms contains form templates
from wtforms import StringField, PasswordField, BooleanField, SubmitField
# validators prevent from submitting empty forms
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    # User and password fields are required
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    # Remember me check
    remember_me = BooleanField('Remember Me')
    # Submit button
    submit = SubmitField('Sign In')
