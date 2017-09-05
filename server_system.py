"""
    Server system file
    Version 0.0.1
"""
from random import randint
from survey import Survey

class SurveySystem:
    """ The server system will allow the admin to handle multiple
        different surveys
    """
    def __init__(self):
        self.surveys = {}     # A list of survey objects
        self.surveys_map = {} # Dictionary to map surveys

    def get_survey_template(self, survey_id):
        """ Return the survey requested """
        survey_id = int(survey_id)
        return self.surveys[survey_id].get_rendered_template()

    def get_survey_modifiable(self, survey_id):
        """ Return the modifiable version of the survey requested """
        survey_id = int(survey_id)
        return self.surveys[survey_id].get_modify_template()

    def get_survey_list(self):
        """ Get the list of surveys available
        """

        html_template = """
            <div>
                <select name='survey_selection'>
        """

        for key in self.surveys_map:
            html_template += """
                <option value='{survey_id}'>{survey_name}</option>
            """.format(survey_id=self.surveys_map[key], survey_name=key)

        html_template += """
                </select>
                <input type='submit' name='chose_survey' value='Select'/>
            </div>
        """

        return html_template

    def add_survey(self, name):
        """ Adds a survey to the system """
        s_obj = Survey()
        s_uni_id = self.load_unique_id()

        self.surveys[s_uni_id] = s_obj
        self.surveys_map[name] = s_uni_id

    def add_question(self, survey_name, obj_q):
        survey_id = self.surveys_map[survey_name]
        self.surveys[survey_id].add_question(obj_q)

    def mod_question(self, survey_id, q_id, obj_q):
        self.surveys[survey_id].modify_question(q_id, obj_q)

    def load_unique_id(self):
        """ TODO: Add code for this section. It is a stub right now
            using a random number generator. Not reliable
        """
        return randint(0,1000000)
