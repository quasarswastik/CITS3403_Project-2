
import unittest, os
from app import app, db
from app.models import User, QuestionSet, Question, UserAnswers
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required


class UserModelCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'test.db')
        self.app = app.test_client()
        db.create_all()
        u1 = User(id=1, username = 'Jack', email = 'jack@myemail.com', admin = True)   # Create Test user 1
        u2 = User(id=2, username = 'Michael', email = 'michael@outlook.com', admin = False)   # Create Test user 2
        u1.set_password('football')
        u2.set_password('garden')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    # Testing the log in page loads correctly
    def test_login_page_loads(self):
        response = self.app.get('/login', content_type='html/text')
        self.assertTrue(b'Log In' in response.data)  # ensures the correct template was rendered
        self.assertEqual(response.status_code, 200)

    # Testing the text on the Login page is incorrect
    def test_login_page_loads_invalid(self):
        response = self.app.get('/login', content_type='html/text')
        self.assertFalse(b'Welcome' in response.data)

    # Testing the Registration page loads correctly
    def test_registration_page_loads(self):
        response = self.app.get('/register', content_type='html/text')
        self.assertTrue(b'Register' in response.data)  # ensures the correct template was rendered
        self.assertEqual(response.status_code, 200)

    # Testing the text on the Registration page is incorrect
    def test_registration_page_loads_invalid(self):
        response = self.app.get('/register', content_type='html/text')
        self.assertFalse(b'Welcome' in response.data)

    # Testing Registration of a new user
    def test_user_registration(self):
        response = self.app.post('/register', data=dict(
            username='Joe', email = 'joe222@gmail.com', 
            password = 'great', password_2 = 'great', 
            administrator = 'True'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    # Test login of user in database
    def test_user_login(self):
        response = self.app.post('/login', data=dict(
            username='Jack', password='football', remember_me=False), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Testing log-out
    def test_valid_logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Testing that the password hashing method is working
    def test_password_hashing(self):
        u1 = User.query.get('1')
        u2 = User.query.get('2')
        self.assertTrue(u1.check_password('football'))
        self.assertTrue(u2.check_password('garden'))
        self.assertFalse(u1.check_password('not_football'))
        self.assertFalse(u2.check_password('not_garden'))

    # Testing administrator attribute for Users
    def test_administrator(self):
        u1 = User.query.get('1')
        u2 = User.query.get('2')
        self.assertEqual(u1.admin, True)
        self.assertEqual(u2.admin, False)
    
    # Tests that an error message is received if a new user tries to register with the same username of a different user
    def test_unique_username(self):
        response = self.app.post('/register', data=dict(
            username='Jack', email = 'joe222@gmail.com', 
            password = 'great', password_2 = 'great', 
            administrator = 'True'), follow_redirects=True)
        self.assertTrue(b'Please use a different username' in response.data)

    # Tests that an error message is received if a new user tries to register with the same email address of a different user
    def test_unique_email(self):
        response = self.app.post('/register', data=dict(
            username='Mike', email = 'michael@outlook.com', 
            password = 'great', password_2 = 'great', 
            administrator = 'True'), follow_redirects=True)
        self.assertTrue(b'Please use a different email address' in response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)