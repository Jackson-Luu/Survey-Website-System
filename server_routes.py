# Survey flask server file
from flask import Flask, flash, redirect, render_template, request, url_for
from server_system import SurveySystem
from server import APP, G_SURVEY_SYSTEM
import csv

# Create a dictionary and initialize ?admin? as a key with
# value = admin's chosen password
USERS = {"admin":"password"}
selected = []
system = SurveySystem()
system.new_admin("admin", "password")

@APP.route("/", methods=["GET", "POST"])
def survey_homepage():
    """ The function to render the homepage
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_password(username, password):
            system.set_admin(username)
            system.load_surveys()
            system.load_results()               
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
		try:
		   if request.form["btn"] == "create":
			   print(request.form["q_type"])
			   system.create_question(request.form["question_box"], request.form["q_type"])
		   elif request.form["btn"] == "survey":
			   return redirect(url_for('create_survey'))
		   elif request.form["btn"] == "pool":
			   return redirect(url_for('show_q'))
		   elif request.form["btn"] == "view_survey":
			   return redirect(url_for('view'))
		except KeyError:
			flash("Please login again.")
			return redirect(url_for('survey_homepage'))
	#return redirect(url_for('admin_survey', survey_id=requested_survey))
	#to_be_rendered = G_SURVEY_SYSTEM.get_survey_list()
	return render_template("admin.html")#, render_test=to_be_rendered)

#@APP.route("/admin/<survey_id>")
#def admin_survey(survey_id):
#    """ Direct link to a survey
#    """
#    to_be_rendered = G_SURVEY_SYSTEM.get_survey_modifiable(survey_id)
#    return render_template("admin.html", render_test=to_be_rendered)

@APP.route("/admin/questions")
def show_q():
    return render_template("questions.html", q_bank=system.get_questions())

@APP.route("/admin/survey", methods=["GET", "POST"])
def create_survey():
    global selected
    if request.method == "POST":
        if request.form["btn"] == "done":
            system.create_survey(set(selected), request.form["s_name"])
            return redirect(url_for('admin'))
        selected.append(int(request.form["btn"]) - 1)
    return render_template("survey.html", q_bank=system.get_questions())

@APP.route("/survey/<survey_id>", methods=["GET", "POST"])
def survey(survey_id):
    s = system.get_survey(int(survey_id))
    if s == None:
        return redirect(url_for('survey_homepage'))
    else:
        if request.method == "POST":
            if request.form["btn"] == "submit":
                answers = []
                for i in range(1, len(s)+1):
                    answers.append(int(request.form[str(i)]))
                system.record_answers(answers, int(survey_id))
                return render_template("submit.html")
        return render_template("user_survey.html", q_bank=s)

@APP.route("/admin/view")
def view():
    s_list = system.get_surveys()
    return render_template("view_survey.html", surveys=s_list)
