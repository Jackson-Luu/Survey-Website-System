"""
    In this server.py, we will handle all of the server side issue
    with python
"""
from flask import Flask
from global_api import QuestionType
from question import Question

APP = Flask(__name__)
APP.config["SECRET_KEY"] = "Highly secret key"
