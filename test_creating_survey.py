''' test creating survey
	user story - 3 '''
	
import unittest
import os
from SurveyManager import *
from sqlalchemy import exc, orm

class test_create_survey(unittest.TestCase):

	def setUp(self):
		self.SurveyManager = create_survey()
	
	''' test - no input is provided'''
  
	def test_no_input(self):
		with self.asseryRaises(TypeError):
			self.SurveyManager.create_survey(datapacket, 0, 0, 0, 0)
  
	''' test - correct input is provided'''
 
	def test_successful_input(self):
		self.SurveyManager.create_survey(datapacket, 1, 'Comp9844', '''quesionlist''', '''state''')
  
	''' test - a duplicate id is provided'''
  
	def test_duplicate_survey_id(self):
		self.SurveyManager.create_survey(datapacket, 1, 'Seng4920', '''quesionlist''', '''state''')
		with self.assertRaises(exc.IntegrityError):
			self.SurveyManager.create_survey(datapacket, 1, 'Seng4920', '''quesionlist''', '''state''')
  
	''' test - duplicate course offering is provided'''
  
	def test_duplicate_course(self):
		self.SurveyManager.create_survey(datapacket, 2, 'Comp9844', '''quesionlist''', '''state''')
		with self.assertRaises(exc.IntegrityError):
			self.SurveyManager.create_survey(datapacket, 2, 'Comp9844', '''quesionlist''', '''state''')
  
	''' test - question from mandatory pool is provided'''
  
	def test_add_question_mandatory(self):
  
	''' test - question from optional pool is provided'''
  
	def test_add_question_optional(self):
  
	''' test - question from mandatory pool is deleted'''
  
	def test_delete_question_mandatory(self):
  
	''' test - question from optional pool is deleted '''
  
	def test_delete_question_optional(self):
  
  
  