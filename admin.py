class admin:
    """Common class for all admins
       Attributes: name, username and password
       given at the time of registration.
    """
  
    #Constructor
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._question_bank = []
        self._survey_list = []

    def add_question(self, question):
        self._question_bank.append(question)

    def get_questions(self):
        return self._question_bank

    def get_question(self, i):
        return self._question_bank[i]

    def add_survey(self, s):
        self._survey_list.append(s)

    def get_surveys(self):
        return self._survey_list

    def set_surveys(self, surveys):
        self._survey_list = surveys;
        
