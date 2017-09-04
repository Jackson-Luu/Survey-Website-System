"""
    This file will handle the survey object
    Version 0.0.1
    The following features that need to be implemented:
        - Split the questions into different web pages when there are
          a lot of them
"""
from global_api import QuestionType

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
    def __init__(self, list_of_q):
        self.list_of_q = list_of_q
        self.render_template = []

    def show_questions(self):
        """ Render the question to the user by forming the HTML in here
        """

        for question in self.list_of_q:
            """ We are first going to load the queston text into the
                template
            """

            input_area = "" # Initialise the variable to prevent errors

            if question.get_type() == QuestionType.TEXT:
                input_area = """
                    <textarea class='q_textinput'>
                        Please enter our input here ...
                    </textarea>
                """
            elif question.get_type() == QuestionType.MULT:
                """ If the question type is multiple choice, we will
                    need to loop through the inputs specified by the
                    admin and format it into the correct html
                """

                # This is used to separate the radio buttons into their groups
                radio_counter = 0
                for q_option in question.get_ans():
                    input_area += """
                        <div class='radio_group'>
                            <div class='radio_btn'>
                                <input type='radio' value='' name='q{counter}'/>
                            </div>
                            <div class='radio_text'>
                                {text}
                            </div>
                        </div>
                    """.format(text=q_option, counter=radio_counter)
                    radio_counter += 1

            template = """
                <fieldset class='q_box'>
                    <div class='q_text'>
                        {q_text}
                    </div>
                    <div class='q_area'>
                        {q_area}
                    </div>
                </fieldset>
            """.format(q_text=question.get_text(), q_area=input_area)

            self.render_template.append(template)
