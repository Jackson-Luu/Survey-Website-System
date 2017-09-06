# Survey flask server file
from flask import Flask, flash, redirect, render_template, request, url_for
from server_system import SurveySystem
from server import APP, G_SURVEY_SYSTEM
from question import Question
from global_api import QuestionType
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
            num_q = G_SURVEY_SYSTEM.get_num_question(survey_id)
            for x in range(0, num_q):
                nvn0 = request.form["the_question_" + str(x)]

                nvn2 = Question(nvn0)
                nvn2.set_type(QuestionType.TEXT)
                G_SURVEY_SYSTEM.mod_question(survey_id, x, nvn2)

    to_be_rendered = G_SURVEY_SYSTEM.get_survey_modifiable(survey_id)
    return render_template("admin.html", render_test=to_be_rendered)

@APP.route("/survey/<survey_id>", methods=["GET", "POST"])
def show_survey(survey_id):
    """ Direct link to a survey
    """
    if request.method == "POST":
        request_value = request.form["btn_sub"]
        if request_value == "Submit":
            with open('storage/response.csv', 'a') as csvfile:
                num_q = G_SURVEY_SYSTEM.get_num_question(survey_id)
                for x in range(0, num_q):
                    foo = request.form["q_user_input_" + str(x)]
                    responsewriter = csv.writer(csvfile)
                    responsewriter.writerow([foo])

    to_be_rendered = G_SURVEY_SYSTEM.get_survey_template(survey_id)
    return render_template("admin.html", render_test=to_be_rendered)
