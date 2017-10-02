from modules.head import *
from modules.DataPacket import DataPacket

def read_questions(data_packet):
    """ We are going to go through the list of questions and translate it
        into something that can rendered into the templates
    """
    renderable = []
    data_list = data_packet.retrieve_data()
    for data in data_list:
        type_text = ""
        type_enum = QuestionType(int(data[2]))

        if type_enum == QuestionType.TEXT:
            type_text = "Text Response"
        elif type_enum == QuestionType.BOOL:
            type_text = "True or False"
        elif type_enum == QuestionType.RATI:
            type_text = "Numeric Rating"
        elif type_enum == QuestionType.RATS:
            type_text = "Text Rating"

        renderable.append([data[0], data[1], type_text])

    return renderable

def create_question(data_packet, question_id, question_text, question_type):
    """ We are going to get the raw data and convert it into a question
        object which we will return
    """
    type_enum = 0 # Default it to the first type

    if question_type == "boolean":
        type_enum = 1
    elif question_type == "rating_int":
        type_enum = 2
    elif question_type == "rating_text":
        type_enum = 3

    data_packet.add_data([question_id, question_text, type_enum])

    return data_packet

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