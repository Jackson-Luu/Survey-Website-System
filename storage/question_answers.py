import csv
from flask import Flask, redirect, render_template, request, url_for
from server import app, user_input

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        question = request.form["question"]
        a1 = request.form["a1"]
        a2 = request.form["a2"]
        a3 = request.form["a3"]
        a4 = request.form["a4"]
        
        user_input.append([question, a1, a2, a3, a4])
        
        return redirect(url_for("question"))
    return render_template("index.html")

@app.route("/Question")
def question():
	question = user_input[0][0]
	a1 = user_input[0][1]
	a2 = user_input[0][2]
	a3 = user_input[0][3]
	a4 = user_input[0][4]
	return render_template("question.html", question=question, a1=a1, a2=a2, a3=a3, a4=a4)


#write to csv
with open('question_answer.csv','a') as csv_out:
	writer = csv.writer(csv_out)
	writer.writerow([question, a1, a2, a3, a4])
    
#read from csv
with open('question_answer.csv','r') as csv_in:
	reader = csv.reader(csv_in)
	for row in reader:
		print(row)
