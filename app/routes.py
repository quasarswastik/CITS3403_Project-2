from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, QuestionEntryForm, QuestionSetEntryForm, SetSelect, DeleteUserForm, DeleteQuestionSetsForm, AdminUserResultsForm
# this is for user login
from flask_login import current_user, login_user, logout_user
# this is the databse required here
from app.models import User, Question, UserAnswers, QuestionSet, AnswerSet
# for pages where login is mandatory
from flask_login import login_required
# helps in redirecting traffic
from werkzeug.urls import url_parse
from numpy import random # used for randomizing question display order

@app.route('/')
@app.route('/theme')
@login_required # this will force login to access the page
def theme():
    # # Page renders the code in the HTML template
    return render_template('theme.html', title = 'Theme')

@app.route('/index')
@login_required # this will force login to access the page
def index():
    # limits access to this page if the user is not an Administrator
    if not current_user.admin:
        flash('You do not have access to that page')
        return redirect(url_for('login'))

    # Fetch all users
    users = User.query.all()
    questions = Question.query.all()
    answers = UserAnswers.query.all()
    c_answers = UserAnswers.query.filter_by(userId=current_user.id).all()
    questionSets = QuestionSet.query.all()
    answerSets = AnswerSet.query.all()
    return render_template('index.html', title = 'Home', users = users, questions = questions, answers=answers, c_answers=c_answers, questionSets=questionSets, answerSets=answerSets)

@app.route('/test_history')
@login_required # this will force login to access the page
def test_history():
    asets = AnswerSet.query.filter_by(user_id=current_user.id).all()
    return render_template('test_history.html', title = 'Attempts', asets=asets)


@app.route('/taketest/', methods=['GET', 'POST'])
@login_required # this will force login to access the page
def take_test():
    questions = Question.query.all()
    sets = QuestionSet.query.all()
    form = SetSelect()
    form.sets.choices = [(s.set_id, s.set_name) for s in sets]
    form.sets.choices.insert(0, (0,''))
    noSet = True
    activeQSet = 0
    activeQSetName = "None Selected"
    randomizedQuestions = []

    if form.validate_on_submit():
        if form.sets.data == 0:
            # blank, display no questions
            noSet = True
        else:
            activeQSet = form.sets.data
            activeQSetName = QuestionSet.query.get(activeQSet).set_name
            questions = QuestionSet.query.get(activeQSet).questions
            noSet = False            

            for idx, question in enumerate(questions):
                answers = [question.correctAnswer, question.answer2, question.answer3, question.answer4]
                qOrder = random.permutation(4)
                randomizedQuestions.append({
                    'question_id': question.question_id,
                    'body': question.body,
                    'a1': answers[qOrder[0]],
                    'a2': answers[qOrder[1]],
                    'a3': answers[qOrder[2]],
                    'a4': answers[qOrder[3]]
                })

    return render_template('q_answers.html', title = 'Test', questions=randomizedQuestions, sets=sets, form=form, noSet=noSet, activeQSet=activeQSet, activeQSetName=activeQSetName)

@app.route('/postanswers/', methods=['POST'])
@login_required
def postanswers():
    activeQSet = request.form["qSet"]
    questions = QuestionSet.query.get(activeQSet).questions
    aset = AnswerSet(user_id = current_user.id, qset_id = activeQSet)

    # create answer records and associate them with an answer set
    for question in questions:
        name = str(question.question_id) + "_answer"
        checked = request.form[name]
        user_response = UserAnswers(userId = current_user.id, questionId = question.question_id, answer = checked)
        db.session.add(user_response)
        aset.answers.append(user_response)

    aset.computeScore()
    db.session.add(aset)
    db.session.commit()

    return redirect(url_for('results'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('theme'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        logged_in_user = user.id
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('theme')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


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

@app.route('/add_questions', methods=['GET', 'POST'])
@login_required # this will force login to access the page
def add_questions():
    # limits access to this page if the user is not an Administrator
    if not current_user.admin:
        flash('You do not have access to that page')
        return redirect(url_for('login'))

    form = QuestionEntryForm()
    if form.validate_on_submit():
        question = Question(body = form.body.data, correctAnswer=form.correctAnswer.data, answer2=form.answer2.data,
                            answer3=form.answer3.data, answer4=form.answer4.data)
        db.session.add(question)
        db.session.commit()
        flash('Question has been set')
        return redirect(url_for('add_questions'))
    return render_template('admin_add_questions.html', title = 'Admin - Add Questions', form = form)

@app.route('/add_set', methods=['GET', 'POST'])
@login_required # this will force login to access the page
def add_set():
    # limits access to this page if the user is not an Administrator
    if not current_user.admin:
        flash('You do not have access to that page')
        return redirect(url_for('login'))

    form = QuestionSetEntryForm()
    form.questions.choices = [(q.question_id, q.body) for q in Question.query.all()]
    if form.validate_on_submit():
        set = QuestionSet(set_name = form.questionset.data, creator_id = current_user.id)
        for q_id in form.questions.data:
            set.questions.append(Question.query.get(q_id))
        db.session.add(set)
        db.session.commit()
        flash('Question Set has been added')
        return redirect(url_for('add_set'))
    return render_template('add_set.html', title = 'Admin - Add Question Sets', form = form)

@app.route('/add_users', methods=['GET', 'POST'])
@login_required
def add_users():
    # limits access to this page if the user is not an Administrator
    if not current_user.admin:
        flash('You do not have access to that page')
        return redirect(url_for('login'))

    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username = form.username.data, email=form.email.data, admin = False)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('New User, {}, has been successfully created!'.format(form.username.data))
        return redirect(url_for('add_users'))
        
    return render_template('admin_add_users.html', title = 'Admin - Add Users', form = form)

@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    asets = AnswerSet.query.filter_by(user_id=current_user.id)
    return render_template('results.html', title = 'Results', asets=asets)

@app.route('/authors')
def authors():
    # Page renders the code in the HTML template
    return render_template('authors.html', title = 'Authors')

@app.route('/delete_users/', methods=['GET', 'POST'])
@login_required
def delete_users():
    if not current_user.admin:
        flash('You do not have access to that page')
        return redirect(url_for('login'))

    form = DeleteUserForm()
    form.users.choices = [(u.id, u.username) for u in User.query.all()]
    
    if form.validate_on_submit():
        for q_id in form.users.data:
            User.query.filter_by(id=q_id).delete()
        db.session.commit()
        flash('User(s) deleted successfully.')
        return redirect(url_for('delete_users'))

    return render_template('delete_user.html', title = 'Admin - Delete Users', form = form)

@app.route('/delete_sets/', methods=['GET', 'POST'])
@login_required
def delete_sets():
    if not current_user.admin:
        flash('You do not have access to that page')
        return redirect(url_for('login'))

    form = DeleteQuestionSetsForm()
    form.sets.choices = [(s.set_id, s.set_name) for s in QuestionSet.query.all()]
    
    if form.validate_on_submit():
        for s_id in form.sets.data:
            QuestionSet.query.filter_by(set_id=s_id).delete()
        db.session.commit()
        flash('Set(s) deleted successfully.')
        return redirect(url_for('delete_users'))

    return render_template('delete_set.html', title = 'Admin - Delete Question Sets', form = form)

@app.route('/admin_results/', methods=['GET', 'POST'])
@login_required # this will force login to access the page
def admin_results():
    # limits access to this page if the user is not an Administrator
    if not current_user.admin:
        flash('You do not have access to that page')
        return redirect(url_for('login'))
    users = User.query.all()
    asets = []
    form = AdminUserResultsForm()
    form.user.choices = [(u.id, u.username) for u in users]
    form.user.choices.insert(0, (0,''))
    noUser = True
    activeUser = 0

    if form.validate_on_submit():
        if form.user.data == 0:
            # blank, display no questions
            noSet = True
            print('yoooo')
        else:
            print('hey')
            activeUser = form.user.data
            asets = AnswerSet.query.filter_by(user_id=activeUser)
            noSet = False

    return render_template('admin_results.html', title = 'View Results', asets=asets, form=form, noUser=noUser)

@app.route('/stats')
def stats():
    qsets = QuestionSet.query.all()
    data = []
    avg = 0
    for qset in qsets:
        if qset.asets.first() is not None:
            maxScore = float(qset.asets.first().score)
            minScore = float(qset.asets.first().score)
            for a in qset.asets.all():
                avg += float(a.score)
                if float(a.score) > maxScore:
                    maxScore = float(a.score)
                elif float(a.score) < minScore:
                    minScore = float(a.score)
            avg = avg/len(qset.asets.all())
            data.append({
                'set_name': qset.set_name,
                'attempts': len(qset.asets.all()),
                'avg': avg,
                'max': maxScore,
                'min': minScore
            })
            avg=0
    return render_template('questionset_stats.html', title = 'Question Set Stats', data=data)
