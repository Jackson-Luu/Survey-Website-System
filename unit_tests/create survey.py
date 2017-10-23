import unittest
import os
from SurveyManager import *
from sqlalchemy import exc, orm

class test_create_survey(unittest.TestCase):

  def test_no_input(self):
    with self.asseryRaises(TypeError):
      self.SurveyManager.create_survey('0', '0', '0', '0', '0')
  
  def test_successful_input(self):
    self.SurveyManager.create_survey('''datapacket''', '1', 'Comp9844', '''quesionlist''', '''state''')
    
  def test_duplicate_survey_id(self):
    self.SurveyManager.create_survey('''datapacket''', '1', 'Seng4920', '''quesionlist''', '''state''')
    with self.assertRaises(exc.IntegrityError):
      self.SurveyManager.create_survey('''datapacket''', '1', 'Seng4920', '''quesionlist''', '''state''')
  
  def test_duplicate_course(self):
    self.SurveyManager.create_survey('''datapacket''', '2', 'Comp9844', '''quesionlist''', '''state''')
    with self.assertRaises(exc.IntegrityError):
      self.SurveyManager.create_survey('''datapacket''', '2', 'Comp9844', '''quesionlist''', '''state''')
  
  
  
  
  
