# CITS3403: Agile Web Development Project 2020

This project is developed for the unit Agile Web Development at The University of Western Australia. For this project we were required to build a multi-user quiz/questionaire/survey application. The application allows administrators to set question sets, users to submit answers to the questions, and manual or automatic assessment of those answers. The context of the questions have flexibility and are upto administrators to decide.

## Purpose

This application can be used for Buzzfeed style quizzes in education sector. Administrators (such as teachers and unit coordinators) can add questions and create question sets. Users (students) of the application can start a question set and complete questions. The answers by the users can be viewed and the results of the assessments are made available.

## Authors

- [Adam Inskip](https://github.com/inskippy)
- [Craig Huggins](https://github.com/craighuggins)
- [Swastik Raj Chauhan](https://github.com/quasarswastik)

## Architecture

The client-side of the web application is designed using HTML, CSS and JavaScript. The server-side is made using Flask micro web framework in Python and the database is developed on SQLite. 

A single web server and a single database is used. In the current architecture, a user sends a request to the web server via HTML forms which are rendered from Jinja2 Templates. The request sent by the users are received by web server and depending on the request, the content is delivered. There can be requests to render plain webpages, fetch information from the database and display to the user or to take input from the user and update the database.

## Database Schema

![Schema](https://github.com/quasarswastik/CITS3403_Project-2/blob/master/Schema_rough.png)

## Launching the application

- Ensure that all the libraries required for this web application are upto date. Use ```pip install -r /path/to/requirements.txt``` to install all the libraries.
- To run the web server application, use ```flask run```

## Unit tests

Unit tests have been added in tests.py, and can by run easily with ```python tests.py```


<span style="text-decoration: underline">Unit Test Descriptions:</span>
```Python
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
```


Additional testing database is available.

## Agile Development Methodolgy

Git was used to develop the application and GitHub was used to host the Git repository.

The project was broken down into small manageable chunks and basic work was divided among all the team members. Once the basic functionality was achieved, testing was done for all the components. Basic functionalty was further enchanced once it was made sure that there are no bugs found. This process was repeated until the end result was developed. Designing was a done simultaneously and all the designing was done in an iterative manner giving consideration to compatibility.

Our first goal was to just develop a basic application in which users can register, it was followed by allowing users to answer pre-fed questions. Having many steps in between, now, users can register themselves, they can either be normal users or with administrator privileges, question sets and questions can be created, users can take those quizzes, correct solutions and previous results can be viewed, these are just some of the features of the application among many other.

We initially decided to split the tasks based on technologies which we are comfortable with. As we progressed thrugh the roles blurred and we were all making contributions as needed for the healthy development.

## Dependencies

- Python 3.x
  - Flask
  - Numpy
  - Werkzeug
  - Selenium
  - Jinja2
  - WTForms
- SQLite
- HTML5
- CSS3
  - Bootstrap 
  - Font Awesome
  - Google Fonts
- JavaScript
  - JQuery

## Screenshots

![Image of home page](https://github.com/quasarswastik/CITS3403_Project-2/blob/master/HomePage.png)
![Image of taketest page](https://github.com/quasarswastik/CITS3403_Project-2/blob/master/TakeTest.png)
![Image of testhistory page](https://github.com/quasarswastik/CITS3403_Project-2/blob/master/TestHistory.png)
![Image of results page](https://github.com/quasarswastik/CITS3403_Project-2/blob/master/Results.png)
