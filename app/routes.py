from flask import render_template
from app import app

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
            'username': 'Frank'
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