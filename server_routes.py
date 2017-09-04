# Survey flask server file
from flask import Flask, flash, redirect, render_template, request, url_for
from server import app
import csv

# Create a dictionary and initialize ?admin? as a key with
# value = admin's chosen password
users = {"admin":"password"}

@app.route("/", methods=["GET", "POST"])

def survey_homepage():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		
		if check_password(username, password):
			return redirect(url_for('admin'))
	return render_template("templates/ui.html")


def check_password(user_name, password):
	"""
 	:param user_name: The name of the user
 	:param password: Password provided by the user
 	"""
	if user_name in users:
		if password == users[user_name]:
			return True

@app.route("/admin")
def admin():
	return render_template("templates/admin.html")
