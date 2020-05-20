from app import db, login
# for passwords hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# User class is inherited from databse model
# All necessary fields are added as db column
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean)
    answers = db.relationship('UserAnswers', backref='user', lazy='dynamic')

    # tells how to display/print objects of this class, creates a format to follow for Python
    def __repr__(self):
        return '<User {}>'.format(self.username)    

    # for storing passwords properly
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# for logging in the user
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# -------- possible implementation for collating questions into quizzes --------------
# # Quiz is a set of question (one quiz to many questions relationship)
# class Quiz(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     setName = db.Column(db.String(120), index=True)
#     questions = db.relationship('Question', backref='quiz', lazy='dynamic')

#     def __repr__(self):
#         return '<Question Set: {}'.format(self.setName)
# ------------------------------------------------------------------------------------

# helper table for many-to-many questionset-to-questions relationship
qset_q_assoc = db.Table('Quizzes',
    db.Column('set_id', db.Integer, db.ForeignKey('question_set.set_id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.question_id'), primary_key=True)
)

class QuestionSet(db.Model):
    set_id = db.Column(db.Integer, primary_key=True)
    set_name = db.Column(db.String(64))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    questions = db.relationship('Question', secondary=qset_q_assoc)
    asets = db.relationship('AnswerSet', backref='qset', lazy='dynamic')

    def __repr__(self):
        return '<Question Set {}'.format(self.set_name)


# Question has text, a correct answer, three false answers
class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256), index=True)
    # don't need to index the answers, all lookups will be for the question itself
    correctAnswer = db.Column(db.String(64))
    answer2 = db.Column(db.String(64))
    answer3 = db.Column(db.String(64))
    answer4 = db.Column(db.String(64))

    # tells how to display/print objects of this class, creates a format to follow for Python
    def __repr__(self):
        return '<Question {}, {}>'.format(self.question_id, self.body) 

# helper table for many-to-many questionset-to-questions relationship
aset_a_assoc = db.Table('Answer Sets',
    db.Column('set_id', db.Integer, db.ForeignKey('answer_set.set_id'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('user_answers.id'), primary_key=True)
)

class UserAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    questionId = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    # store user's selected answer as the string value of the selected answer
    answer = db.Column(db.String(64))
    setID = db.Column(db.Integer, db.ForeignKey('question_set.set_id'))

    # tells how to display/print objects of this class, creates a format to follow for Python
    def __repr__(self):
        return '<User answer {}, {}, {}, {}>'.format(self.id, self.userId, self.questionId, self.answer) 

class UserAttempts(db.Model):
    attempt_id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    numberCorrect = db.Column(db.Integer)
    numberIncorrect = db.Column(db.Integer)
    score = db.Column(db.String(4))
    timeOfAttempt = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<User Attempt {}, {}, {}, {}, {}, {}>'.format(self.attempt_id, self.userId, self.numberCorrect, self.numberIncorrect, self.score, self.timeOfAttempt)

class AnswerSet(db.Model):
    set_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    qset_id = db.Column(db.Integer, db.ForeignKey('question_set.set_id'))
    answers = db.relationship('UserAnswers', secondary=aset_a_assoc)

    def __repr__(self):
        return '<Question Set {}'.format(self.set_name)