from flask import Flask
from config import Config
# the following 2 are for databases
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# for user logins
from flask_login import LoginManager

# Creates the application object as an instance of class Flask
app = Flask(__name__)
app.config.from_object(Config)

# db represents database, migrate represents migration object (would be needed for migrating database)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

# importing routes for proper routes and models for all database models
from app import routes, models