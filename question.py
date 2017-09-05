"""
    This file will set up the class that will handle question objects
    Version 0.0.1
"""
from global_api import QuestionType

class Question:
    """ The question object """
    def __init__(self, q_text):
        self.q_text = q_text # The question itself. E.G "What is your favourite dog"
        # Set the type of question it is
        self.q_type = QuestionType.NULL
        self.q_ans = []      # The answers available for the questions.

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

    def add_ans(self, s_ans):
        """ Adds a possible answer """
        self.q_ans.append(s_ans)
        return

    def set_type(self, q_type):
        """ Sets the type of question """
        self.q_type = q_type

    def set_text(self, q_text):
        """ Sets the question """
        self.q_text = q_text
