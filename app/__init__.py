from flask import Flask

# Creates the application object as an instance of class Flask
app = Flask(__name__)

from app import routes