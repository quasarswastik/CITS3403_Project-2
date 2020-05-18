from app import app, db
from app.models import User, Question, UserAttempts, UserAnswers # for now we only import user, as the tables increase, we will add more stuf to it

# this is useful for testing using shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Question': Question, 'UserAnswers': UserAnswers, 'UserAttempts': UserAttempts}