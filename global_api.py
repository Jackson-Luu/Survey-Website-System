"""
    This file will contain the variables or objects that will carry
    over through all files. This will help standarise the whole project
    Version 0.0.1
"""
from enum import Enum

class QuestionType(Enum):
    """ This is is just to standarise the question types across the
        files.
    """
    NULL = -1 # Question type not set
    TEXT =  0 # The question is text based
    MULT =  1 # The question is multiple choice based
    DROP =  2 # The question is drop down based
