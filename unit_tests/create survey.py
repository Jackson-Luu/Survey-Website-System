import unittest
import os
from SurveyManager import *
from sqlalchemy import exc, orm

''' user story: 3 '''

class test_create_survey(unittest.TestCase):

  def setUp(self)

  ''' testing when no input is provided'''
  
  def test_no_input(self):
    with self.asseryRaises(TypeError):
      self.SurveyManager.create_survey('0', '0', '0', '0', '0')
  
  ''' testing when correct input is provided'''
 
  def test_successful_input(self):
    self.SurveyManager.create_survey('''datapacket''', '1', 'Comp9844', '''quesionlist''', '''state''')
  
  ''' testing when a duplicate id is provided'''
  
  def test_duplicate_survey_id(self):
    self.SurveyManager.create_survey('''datapacket''', '1', 'Seng4920', '''quesionlist''', '''state''')
    with self.assertRaises(exc.IntegrityError):
      self.SurveyManager.create_survey('''datapacket''', '1', 'Seng4920', '''quesionlist''', '''state''')
  
  ''' testing when a duplicate course offerring is provided'''
  
  def test_duplicate_course(self):
    self.SurveyManager.create_survey('''datapacket''', '2', 'Comp9844', '''quesionlist''', '''state''')
    with self.assertRaises(exc.IntegrityError):
      self.SurveyManager.create_survey('''datapacket''', '2', 'Comp9844', '''quesionlist''', '''state''')
  
  ''' testing when a question from mandatory pool is provided'''
  
  def test_add_question_mandatory(self):
  
  ''' testing when a question from optional pool is provided'''
  
  def test_add_question_optional(self):
  
  ''' testing when a question from mandatory pool is deleted'''
  
  def test_delete_question_mandatory(self):
  
  ''' testing when a question from optional pool is deleted '''
  
  def test_delete_question_optional(self):
  
  
