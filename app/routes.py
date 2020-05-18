from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import QuestionEntryForm
# this is for user login
from flask_login import current_user, login_user, logout_user
# this is the databse required here
from app.models import User, Question, UserAnswers
# for pages where login is mandatory
from flask_login import login_required
# helps in redirecting traffic
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required # this will force login to access the page
def index():
    # Fetch all users
    users = User.query.all()
    questions = Question.query.all()
    answers = UserAnswers.query.all()
    c_answers = UserAnswers.query.filter_by(userId=current_user.id).all()
    return render_template('index.html', title = 'Home', users = users, questions = questions, answers=answers, c_answers=c_answers)


@app.route('/taketest/', methods=['GET', 'POST'])
@login_required # this will force login to access the page
def take_test():
    # Mock Questions
    questions = Question.query.all()

    return render_template('q_answers.html', title = 'Test', questions = questions)

@app.route('/postanswers/', methods=['POST'])
@login_required
def postanswers():
    questions = Question.query.all()
    for question in questions:
        name = str(question.question_id) + "_answer"
        checked = request.form[name]
        user_response = UserAnswers(userId = current_user.id, questionId = question.question_id, answer = checked)
        db.session.add(user_response)
        db.session.commit()
    return redirect(url_for('index'))

# @app.route('/admin_page')
# @login_required # this will force login to access the page
# def admin_page():
  
#     return render_template('admin_page.html', title = 'Test')


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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email=form.email.data, admin=form.administrator.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks {}, you have been registered as a New User and may now Log In. administrator={}'.format(
            form.username.data, form.administrator.data))
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/admin_page', methods=['GET', 'POST'])
@login_required # this will force login to access the page
def admin_page():
    form = QuestionEntryForm()
    if form.validate_on_submit():
        question = Question(body = form.body.data, correctAnswer=form.correctAnswer.data, answer2=form.answer2.data,
                            answer3=form.answer3.data, answer4=form.answer4.data)
        db.session.add(question)
        db.session.commit()
        flash('Question has been set')
        return redirect(url_for('admin_page'))
    return render_template('admin_page.html', title = 'Admin Page', form = form)

@app.route('/results')
def results():
    questions = Question.query.all()
    answers = UserAnswers.query.filter_by(userId=current_user.id)

    score = 0
    question_count = len(questions)
    for index, question in enumerate(questions):
        if question.correctAnswer == answers[index].answer:
            score += 1

    return render_template('results.html', title = 'Results', questions=questions, answers=answers, score=score, question_count=question_count)

@app.route('/theme')
def theme():
    # Fetch all users
    return render_template('theme.html', title = 'Theme')

@app.route('/authors')
def authors():
    # Fetch all users
    return render_template('authors.html', title = 'Authors')
