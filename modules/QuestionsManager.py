from modules.head import *
from modules.Question import Question

def read_questions(question_list):
    """ We are going to go through the list of questions and translate it
        into something that can rendered into the templates
    """
    renderable = []
    for q in question_list:
        type_text = ""
        type_enum = q.get_type()

        if type_enum == QuestionType.TEXT:
            type_text = "Text Response"
        elif type_enum == QuestionType.BOOL:
            type_text = "True or False"
        elif type_enum == QuestionType.RATI:
            type_text = "Numeric Rating"
        elif type_enum == QuestionType.RATS:
            type_text = "Text Rating"

        renderable.append([q.get_id(), q.get_text(), type_text])

    return renderable

def create_question(question_id, question_text, question_type):
    """ We are going to get the raw data and convert it into a question
        object which we will return
    """
    type_enum = QuestionType(0) # Default it to the first type

    if question_type == "boolean":
        type_enum = QuestionType(1)
    elif question_type == "rating_int":
        type_enum = QuestionType(2)
    elif question_type == "rating_text":
        type_enum = QuestionType(3)

    question_obj = Question(question_id)
    question_obj.set_text(question_text)
    question_obj.set_type(type_enum)

    return question_obj

class QuestionForm(Form):
    question = TextField('Question', [validators.Required('Please enter a question.')])
    questiontype = SelectField('Select_Field', choices = [('boolean', 'True Or False'), ('text', 'Text'),
                                        ('rating_int', 'Numeric Rating'), ('rating_text', 'Text Rating')])
    add = SubmitField('Add')

class ModifyForm(Form):
    questionid = IntegerField('questionid')
    modquestion = TextField('Question', [validators.Required('Please enter a question.')])
    modquestiontype = SelectField('Select_Field', choices = [('boolean', 'True Or False'), ('text', 'Text'),
                                        ('rating_int', 'Numeric Rating'), ('rating_text', 'Text Rating')])
    mod = SubmitField('Modify')