import csv
from modules.head import *
from modules.DataPacket import DataPacket

def read_surveys(data_packet, admin_perms, courses):
    """ We are going to go through the list of DataPackets and translate it
        into something that can rendered into the templates
    """
    renderable = [] # List to hold the information that can used by Jinja2
    data_list = data_packet.retrieve_data()
    course_list = []
    if courses:
        for course in courses:
            course_list.append(*course)

    for data in data_list:
        # Go through each data and translate it into just 3 strings that can
        # be stored in a list
        if not admin_perms:
            if data[1] in course_list:
                renderable.append([data[0], data[1], data[2], data[3]])
        else:
            renderable.append([data[0], data[1], data[2], data[3]])

    return renderable

def create_survey(data_packet, survey_id, course, question_list, state):
    """ We are going to get the raw data and convert it into a DataPacket
        object which we will return
    """
    questions = ','.join(str(x) for x in question_list)
    data_packet.add_data([survey_id, course, questions, state])

    return data_packet

def get_course_list():
    information = []
    with open("storage/courses.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            row_str = row[0] + ' ' + row[1]
            information.append(row_str)
    return information
