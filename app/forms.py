from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Question

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email    = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Password Repeated', validators=[DataRequired(), EqualTo('password')])
    administrator = BooleanField('Register as an Administrator')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class QuestionEntryForm(FlaskForm):
    body = TextAreaField('Question Body', validators=[DataRequired()])
    choice_1 = StringField('Choice Number 1', validators=[DataRequired()])
    choice_2 = StringField('Choice Number 2', validators=[DataRequired()])
    choice_3 = StringField('Choice Number 3', validators=[DataRequired()])
    choice_4 = StringField('Choice Number 4', validators=[DataRequired()])
    correct_answer = StringField('Correct Answer', validators=[DataRequired()])
    submit = SubmitField('Enter Question')