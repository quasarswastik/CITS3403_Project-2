# CITS3403: Agile Web Development Project 2020

This project is developed for the unit Agile Web Development at The University of Western Australia. For this project we were required to build a multi-user quiz/questionaire/survey application. The application allows administrators to set question sets, users to submit answers to the questions, and manual or automatic assessment of those answers. The context of the questions have flexibility and are upto administrators to decide.

## Purpose

This application can be used for Buzzfeed style quizzes in education sector. Administrators (such as teachers and unit coordinators) can add questions and create question sets. Users (students) of the application can start a question set and complete questions. The answers by the users can be viewed and the results of the assessments are made available.

## Architecture

The client-side of the web application is designed using HTML, CSS and JavaScript. The server-side is made using Flask and the dataase is developed on SQLite. A single web server and a single database is used. In the current architecture, when a user opens the website, the web server responds to the requests with approprite HTML and in general............


## Launching the application

- Ensure that all the libraries required for this web application are upto date. Use ```pip install -r /path/to/requirements.txt``` to install all the libraries.
- To run the web server application, use ```flask run```

## Unit tests

Unit tests have been added in tests.py, and can by run easily with ```python tests.py```

<span style="text-decoration: underline">Unit Test Descriptions:</span>

class UserModelCase(unittest.TestCase):

    setUp(self) method:
    - special method that runs before and after each test
    - ensure that the testing Database is separate is different than the main Database
    - create two users for testing purposes and add them to the database

    tearDown(self) method:
    - resets the contents of the database

    test_login_page_loads(self) method:
    - tests that the log-in page has loaded correctly
    - ensures that the title text 'Log In' appears on the page
    - ensures we received a Response Status Code == 200

    def test_login_page_loads_invalid(self) method:
    - we test that some dummy text does not appear on the page

    def test_registration_page_loads(self) method:
    - tests that the Register page has loaded correctly
    - ensures that the title text 'Register' appears on the page
    - ensures we received a Response Status Code == 200

    def test_registration_page_loads_invalid(self) method:
    - we test that some dummy text does not appear on the page

    def test_user_registration(self) method:
    - tests the registration of a new user
    - ensures we received a Response Status Code == 200

    def test_user_login(self) method:
    - tests the log-in of a user currently in the database
    - ensures we received a Response Status Code == 200

    def test_valid_logout(self) method:
    - tests logout works correctly
    - ensures we received a Response Status Code == 200

    def test_password_hashing(self) method:
    - retrieve the two users from the database
    - run the check_password method to ensure that password hashing worked correctly

    def test_administrator(self) method:
    - retrieve the two users from the database
    - check that each user has the correct 'Administrator' status

    def test_unique_username(self) method:
    - attempt to register a New User with the same username as an existing user in the database
    - check that the appropriate error message is displayed on the page

    def test_unique_email(self) method:
    - attempt to register a New User with the same email address as an existing user in the database
    - check that the appropriate error message is displayed on the page


## Screenshots

![Image of home page](https://github.com/quasarswastik/CITS3403_Project-2/blob/master/HomePage.png)
