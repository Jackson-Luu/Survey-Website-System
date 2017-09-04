"""
    This file will set up the class that will handle question objects
    Version 0.0.1
"""
from global_api import QuestionType

class Question:
    """ The question object """
    def __init__(self, q_type, q_text, q_ans):
        self.q_type = q_type # What type of question is it? Text based or multiple choice base
        self.q_text = q_text # The question itself. E.G "What is your favourite dog"
        self.q_ans = q_ans   # The answers available for the questions. This should be a list!

    def get_type(self):
        """ Return the type of question """
        return self.q_type

    def get_ans(self):
        """ Return the answers that should be available for the
            question
        """
        return self.q_ans

    def get_text(self):
        """ Returns the question """
        return self.q_text

    def add_ans(self):
        """ Adds a possible answer """
        # TODO: Add code for this
        return # Delete after finished

    def set_type(self, q_type):
        """ Sets the type of question """
        self.q_type = q_type
