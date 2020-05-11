from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    administrator_check = BooleanField('Sign up as an Administrator')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')