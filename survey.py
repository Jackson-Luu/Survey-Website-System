"""
    This file will handle the survey object. The survey object will
    just handle the rendering of one particular survey.
    Version 0.0.1
    The following features that need to be implemented:
        - Split the questions into different web pages when there are
          a lot of them
"""
from global_api import QuestionType
from question import Question

class Survey:
    """ The survey class will allow the creation of modular surveys
        that can be distributed to respondants
    """

    """ In the constructor, the survey class will take in a list of
        type Question to manipulate. It will use this list to show the
        questions and to get the responses.

        Also in the constructor, we will set a list to store the HTML
        needed to render the questions.
    """
    def __init__(self, s_id, name):
        self.list_of_q = []
        self.answers = []
        self.id = s_id
        self.name = name

    #def add_question(self, obj_q):
    #    """ Add a question to the survey """
    #    self.list_of_q.append(obj_q)

    def add_question(self, question):
        self.list_of_q.append(question)
        if int(question.get_type()) == 1:
            self.answers.append([0]*5)
        else:
            self.answers.append([0]*2)

    def get_name(self):
        return self.name

    def get_questions(self):
        return self.list_of_q

    def get_id(self):
        return self.id

    def num_questions(self):
        return len(self.list_of_q)

    def get_answers(self):
        return self.answers

    def set_answers(self, answers):
        self.answers = answers

    def modify_question(self, q_id, question):
        """ Modify the question stored in the survey """
        self.list_of_q[q_id] = question
