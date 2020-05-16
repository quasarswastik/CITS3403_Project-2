from app import db, login
# for passwords hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# User class is inherited from databse model
# All necessary fields are added as db column
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean)

    # tells how to display/print objects of this class, creates a format to follow for Python
    def __repr__(self):
        return '<User {}>'.format(self.username)    

    # for storing passwords properly
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256), index=True)
    choice_1 = db.Column(db.String(64))
    choice_2 = db.Column(db.String(64))
    choice_3 = db.Column(db.String(64))
    choice_4 = db.Column(db.String(64))
    correct_answer = db.Column(db.String(64))

    # tells how to display/print objects of this class, creates a format to follow for Python
    def __repr__(self):
        return '<Question {}, {}>'.format(self.question_id, self.body) 


# for logging in the user
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
