""" The file holds all class and functions in aiding the creation of a survey
    manager
"""
import csv
from modules.head import *

def get_course_tuple():
    information = []
    with open("storage/courses.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            information.append(tuple((row[0], row[0])))
    return information

retrieved_courses = get_course_tuple()

class AddSurveyForm(Form):
    survey_name = TextField('survey_name', [validators.Required('Please enter a name for the survey.')])
    survey_courses = SelectField(
        'survey_courses',
        choices=retrieved_courses
    )
    survey_submit = SubmitField('Submit')