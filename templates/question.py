#create questions 
#add options 

from flask import Flask, redirect, render_template, request, url_for
from server import app, user_input

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        answers = request.form["answers"]

        user_input.append([answers])
        return redirect(url_for("answers"))
    return render_template("template(ans).html")

@app.route("/Answers")
def answers():
    return render_template("answers.html", all_users=user_input)