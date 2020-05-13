from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
from app.forms import RegistrationForm
# this is for user login
from flask_login import current_user, login_user, logout_user
# this is the databse required here
from app.models import User
# for pages where login is mandatory
from flask_login import login_required
# helps in redirecting traffic
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required # this will force login to access the page
def index():
    # Mock Users Object
    users = [
        {
            'username': 'Craig'
        },
        {
            'username': 'Swastik'
        },
        {
            'username': 'Adam'
        }
    ]

    return render_template('index.html', title = 'Home', users = users)


@app.route('/taketest')
def take_test():
    # Mock Questions
    questions = [
        {
            'question_number': '1',
            'body': 'What is the capital city of...?'
        },
        {
            'question_number': '2',
            'body': 'What is the sum of the equation'
        }
    ]
    return render_template('q_answers.html', title = 'Test', questions = questions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks {}, you have been registered as a New User and may now Log In. administrator={}'.format(
            form.username.data, form.administrator.data))
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/results')
def results():
    # Mock Questions
    questions = [
        {
            'question_number': '1',
            'body': 'What is the capital city of...?'
        },
        {
            'question_number': '2',
            'body': 'What is the sum of the equation'
        }
    ]
    return render_template('results.html', title = 'Results', questions=questions)