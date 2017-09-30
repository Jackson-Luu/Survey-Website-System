"""
    Here, we are going to create a Question class that will be able to access important
    data without having the rest of the system work with raw data. Thus, we can make changes
    the way we store the raw data without comprising the whole system.
"""
from modules.head import *

class Question():
    """ The question class itself """

    def __init__(self, question_id):
        # The question id number should not change. It should 'permanently' define it
        # during its runtime
        self._question_id = question_id
        self._question_text = ""
        self._question_type = ""

    def set_type(self, question_type):
        """ We are going to set the type of the question using the
            enums.
        """

        # As such, inspect if the variable is of a QuestionType class
        if isinstance(question_type, QuestionType):
            self._question_type = question_type
        else:
            raise Exception("set_type was not given a QuestionType parameter")

    def set_text(self, question_text):
        """ Setting what the question will read """
        self._question_text = question_text

    def get_type(self):
        """ Return the type of question """
        return self._question_type

    def get_text(self):
        """ Get the text of the question """
        return self._question_text

    def get_id(self):
        """ Get the question id """
        return self._question_id
