
import unittest
from app import app, db
from app.models import User, QuestionSet, Question, UserAnswers, UserAttempts

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Helper method for User Registration
    def register(self, username, email, password, password_2, admin):
        return self.app.post(
            '/register',
            data = dict(username = username, email = email, password = password, password_2 = password_2, admin = admin),
            follow_redirects=True
        )


    def test_valid_user_registration(self):
        response = self.register('Craig_H', 'craig.huggins777@gmail.com', 'hidden', 'hidden', 'True')
        self.assertEqual(response.status_code, 200)

    # test password hashing - test should pass with no problem
    def test_password_hashing(self):
        u = User(username = 'Michael', email = 'michael@outlook.com')
        u.set_password('soccer')
        self.assertTrue(u.check_password('soccer'))  # checking that password matches - should be True
        self.assertFalse(u.check_password('cricket'))   # checking that password doesn't match - should be False

    # # test password hashing - this one should fail
    # def test_password_hashing_2(self):
    #     u = User(username = 'Suzanne', email = 'suzanne@outlook.com')
    #     u.set_password('cat')
    #     self.assertTrue(u.check_password('monkey'))  # passwords dont match - assertTrue should return 'false'
    #     self.assertFalse(u.check_password('cat'))   # the correct password - assertFalse should return 'false'

    # testing users have admin priveliges
    def test_administrator(self):
        u1 = User(username = 'Craig', email = 'craig@myemail.com', admin = True)
        u2 = User(username = 'Michael', email = 'michael@outlook.com', admin = False)
        db.session.add_all([u1, u2])
        db.session.commit()
        self.assertEqual(u1.admin, True)
        self.assertEqual(u2.admin, False)




if __name__ == '__main__':
    unittest.main(verbosity=2)