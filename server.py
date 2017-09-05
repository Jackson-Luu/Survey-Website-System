"""
    In this server.py, we will handle all of the server side issue
    with python
"""
from flask import Flask
from server_system import SurveySystem

APP = Flask(__name__)
APP.config["SECRET_KEY"] = "Highly secret key"

# Before the application runs, we need to set up the Survey System
G_SURVEY_SYSTEM = SurveySystem()

# =====
# DEBUG
# =====
# Load up a prebuilt survey to debug, delete when not needed
G_SURVEY_SYSTEM.add_survey("debug1")
