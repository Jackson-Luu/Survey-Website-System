"""
    Server system file
    Version 0.0.1
"""
from random import randint
from survey import Survey
from question import Question
from admin import admin
import pickle

class SurveySystem:
    """ The server system will allow the admin to handle multiple
        different surveys
    """
    def __init__(self):
        self.surveys = {}     # A list of survey objects
        self.surveys_map = {} # Dictionary to map surveys
        self.admins = {}
        self.curr_admin = None

    def get_surveys(self):
        s_list = []
        for s in self.admins[self.curr_admin].get_surveys():
           s_list.append([s.get_name(), "/survey/" + str(s.get_id())])
        return s_list

    def load_unique_id(self):
        """ TODO: Add code for this section. It is a stub right now
            using a random number generator. Not reliable
        """
        rand_id = randint(0, 1000000)
        flag = True
        for key in self.admins:
            for s in self.admins[key].get_surveys():
                if s.get_id == rand_id:
                    flag = False
                    break
            if flag == False:
                break
        if flag == False:
           return load_unique_id()
        else:
           print(rand_id)
           return rand_id

    def create_question(self, text, q_type):
        q = Question(text)
        q.set_type(q_type)
        self.admins[self.curr_admin].add_question(q)

    def set_admin(self, name):
        self.curr_admin = name

    def new_admin(self, username, password):
        self.admins[username] = admin(username, password)

    def get_questions(self):
        return self.admins[self.curr_admin].get_questions()

    def create_survey(self, selection, name):
        s = Survey(self.load_unique_id(), name)
        for i in selection:
            s.add_question(self.admins[self.curr_admin].get_question(i))
        self.admins[self.curr_admin].add_survey(s)
        self.save_surveys()
   
    def get_survey(self, s_id):
        for key in self.admins:
            for s in self.admins[key].get_surveys():
                if s.get_id() == s_id:
                    return s.get_questions()
        return None
    def get_s(self, s_id):
        for key in self.admins:
            for s in self.admins[key].get_surveys():
                if s.get_id() == s_id:
                    return s

    def record_answers(self, answers, survey):
        count = 0
        s = self.get_s(survey)
        for i in answers:
            s.get_answers()[count][i] += 1
            count += 1
        self.save_results()

    def save_surveys(self):
        with open('survey_save.pkl', 'wb') as output:
            pickle.dump(self.admins[self.curr_admin].get_surveys(), output, pickle.HIGHEST_PROTOCOL)

    def load_surveys(self):
        try:
            with open('survey_save.pkl', 'rb') as input:
                self.admins[self.curr_admin].set_surveys(pickle.load(input))
        except FileNotFoundError:
            pass

    def save_results(self):
        with open('results_save.pkl', 'wb') as output:
            for s in self.admins[self.curr_admin].get_surveys():
                pickle.dump(s.get_answers(), output, pickle.HIGHEST_PROTOCOL)
                print(s.get_answers())

    def load_results(self):
        try:
            with open('survey_save.pkl', 'rb') as input:
                for s in self.admins[self.curr_admin].get_surveys():
                    try:
                        s.set_answers(pickle.load(input))
                        print(s.get_answers())
                    except EOFError:
                        break                
        except FileNotFoundError:
            pass          

