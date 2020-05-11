from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, administrator_check={}, remember_me={}'.format(
            form.username.data, form.administrator_check.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title = 'Log In', form = form)