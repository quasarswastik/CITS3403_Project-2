from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField, widgets, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Question, QuestionSet

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
    correctAnswer = StringField('Answer 1 (Correct)', validators=[DataRequired()])
    answer2 = StringField('Answer 2 (Incorrect)', validators=[DataRequired()])
    answer3 = StringField('Answer 3 (Incorrect)', validators=[DataRequired()])
    answer4 = StringField('Answer 4 (Incorrect)', validators=[DataRequired()])
    submit = SubmitField('Enter Question')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class QuestionSetEntryForm(FlaskForm):
    questionset = TextAreaField('Question Set Name', validators=[DataRequired()])
    questions = MultiCheckboxField('Questions to Add', coerce=int)
    submit = SubmitField('Submit Question Set')

    def validate_questionset(self, questionset):
        qset = QuestionSet.query.filter_by(set_name=questionset.data).first()
        if qset is not None:
            raise ValidationError('Please use a different question set name.')

class SetSelect(FlaskForm):
    sets = SelectField('Question Set:', coerce=int)
    submit = SubmitField('Load Question Set')

class DeleteUserForm(FlaskForm):
    users = MultiCheckboxField('Users to Delete', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Delete Users')