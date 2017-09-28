import csv
import os
from modules.head import *

class QuestionForm(Form):
    question = TextField('Question', [validators.Required('Please enter a question.')])
    questiontype = SelectField('Select_Field', choices = [('boolean', 'True Or False'), ('text', 'Text'),
                                        ('rating_int', 'Numeric Rating'), ('rating_text', 'Text Rating')])

def ReadQuestions():
    if os.path.exists('storage/questions.csv'):
        with open('storage/questions.csv') as csvfile:
            listofquestion = []
            questionreader = csv.reader(csvfile)
            for row in questionreader:
                listofquestion.append(row)
        return listofquestion
    else:
        open('storage/questions.csv', 'w').close()
        return []

def AddQuestion(question, questiontype):
    with open('storage/questions.csv', 'a') as csvfile:
        questionwriter = csv.writer(csvfile)
        questionwriter.writerow([question, questiontype])

def DeleteQuestion(questionid):
    counter = 0
    listofquestion = []

    if os.path.exists('storage/questions.csv'):
        with open('storage/questions.csv') as csvfile:
            questionreader = csv.reader(csvfile)
            for row in questionreader:
                if counter != questionid:
                    listofquestion.append(row)
                counter += 1
    
    if len(listofquestion) != 0:
        with open('storage/questions.csv', 'w') as csvfile:
            for row in listofquestion:
                questionwriter = csv.writer(csvfile)
                questionwriter.writerow(row)