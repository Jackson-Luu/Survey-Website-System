# Survey flask server file
from flask import Flask, flash, redirect, render_template, request, url_for
from server_system import SurveySystem
from server import APP, G_SURVEY_SYSTEM
from question import Question
import csv

# Create a dictionary and initialize ?admin? as a key with
# value = admin's chosen password
USERS = {"admin":"password"}

@APP.route("/", methods=["GET", "POST"])
def survey_homepage():
    """ The function to render the homepage
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_password(username, password):
            return redirect(url_for('admin'))
    return render_template("ui.html")

def check_password(user_name, password):
    """
    :param user_name: The name of the user
    :param password: Password provided by the user
    """
    if user_name in USERS:
        if password == USERS[user_name]:
            return True

@APP.route("/admin", methods=["GET", "POST"])
def admin():
    """ This is the function to help render the admin page
    """

    if request.method == "POST":
        requested_survey = request.form["survey_selection"]
        return redirect(url_for('admin_survey', survey_id=requested_survey))

    to_be_rendered = G_SURVEY_SYSTEM.get_survey_list()
    return render_template("admin.html", render_test=to_be_rendered)

@APP.route("/admin/<survey_id>", methods=["GET", "POST"])
def admin_survey(survey_id):
    """ The survey but modifiable for the admin
    """

    if request.method == "POST":
        request_value = request.form["btn_sub"]
        if request_value == "Return":
            return redirect(url_for('admin'))
        elif request_value == "Submit":

    to_be_rendered = G_SURVEY_SYSTEM.get_survey_modifiable(survey_id)
    return render_template("admin.html", render_test=to_be_rendered)

@APP.route("/survey/<survey_id>")
def show_survey(survey_id):
    """ Direct link to a survey
    """
    to_be_rendered = G_SURVEY_SYSTEM.get_survey_template(survey_id)
    return render_template("admin.html", render_test=to_be_rendered)
