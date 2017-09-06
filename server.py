"""
    In this server.py, we will handle all of the server side issue
    with python
"""
from flask import Flask
from server_system import SurveySystem
from global_api import QuestionType
from question import Question

APP = Flask(__name__)
APP.config["SECRET_KEY"] = "Highly secret key"

# Before the application runs, we need to set up the Survey System
G_SURVEY_SYSTEM = SurveySystem()

# =====
# DEBUG
# =====
# Load up a prebuilt survey to debug, delete when not needed
G_SURVEY_SYSTEM.add_survey("debug1")
q1 = Question("What am I doing?")
q1.set_type(QuestionType.TEXT)
G_SURVEY_SYSTEM.add_question("debug1", q1)
q2 = Question("Why is life so hard")
q2.set_type(QuestionType.TEXT)
G_SURVEY_SYSTEM.add_question("debug1", q2)
