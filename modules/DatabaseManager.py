""" 
    The purpose of the database manager is to delegate all of the accessing of data
    to a single class. In doing this, we are able to change how we access the database without
    causing much issue.
"""
import csv
import os
from modules.Question import Question
from modules.head import *

class DBManager():
    """ The class that will create a database manager """
    def __init__(self, file_name):
        self._file_name = file_name
        # Change the file extension if you want to change how the data is stored
        self._file_ext = '.csv'
        self._final_path = 'storage/' + self._file_name + self._file_ext

    def retrieve_data(self):
        """ Here, we are going to access the data and return it as a list """

        if os.path.exists(self._final_path):
            # If the file exists, open it and read the row of data
            with open(self._final_path) as csvfile:
                listofquestion = []
                questionreader = csv.reader(csvfile)

                for row in questionreader:
                    new_q = Question(row[0])

                    new_q.set_text(row[1])
                    new_q.set_type(QuestionType(int(row[2])))

                    listofquestion.append(new_q)

            return listofquestion
        else:
            open(self._final_path, 'w').close()
            return []

    def add_data(self, question):
        """ Here, we are going to add a question to the database """
        if isinstance(question, Question):
            with open(self._final_path, 'a') as csvfile:
                questionwriter = csv.writer(csvfile)
                questionwriter.writerow([question.get_id(), question.get_text(),
                                         question.get_type().value])
        else:
            raise Exception("question given is not of type Question")

    def remove_data(self, questionid):
        """ Delete the data from the database """
        listofquestion = []

        if os.path.exists(self._final_path):
            with open(self._final_path) as csvfile:
                questionreader = csv.reader(csvfile)
                for row in questionreader:
                    if row[0] != questionid:
                        listofquestion.append(row)

        if len(listofquestion) > 0:
            with open(self._final_path, 'w') as csvfile:
                for row in listofquestion:
                    questionwriter = csv.writer(csvfile)
                    questionwriter.writerow(row)
        else:
            open(self._final_path, 'w').close()

    def modify_data(self, question):
        """ Modify the question in the database """
        if isinstance(question, Question):
            listofquestion = []

            if os.path.exists(self._final_path):
                with open(self._final_path) as csvfile:
                    questionreader = csv.reader(csvfile)
                    for row in questionreader:
                        if row[0] != question.get_id():
                            listofquestion.append(row)
                        else:
                            listofquestion.append([question.get_id(), question.get_text(),
                                                   question.get_type().value])

            if len(listofquestion) != 0:
                with open(self._final_path, 'w') as csvfile:
                    for row in listofquestion:
                        questionwriter = csv.writer(csvfile)
                        questionwriter.writerow(row)
        else:
            raise Exception("question given is not of type Question")

    def retrieve_specific(self, question_id_list):
        """ Retrieve a specific list of Questions based on the question id
            listed
        """

        if os.path.exists(self._final_path):
            # If the file exists, open it and read the row of data
            with open(self._final_path) as csvfile:
                listofquestion = []
                questionreader = csv.reader(csvfile)

                for row in questionreader:
                    if row[0] in question_id_list:
                        new_q = Question(row[0])

                        new_q.set_text(row[1])
                        new_q.set_type(QuestionType(int(row[2])))

                        listofquestion.append(new_q)

            return listofquestion
        else:
            open(self._final_path, 'w').close()
            return []
