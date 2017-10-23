''' testing the creation of optional and mandatory questions 
	user story - 4 '''

import unittest
import os
from QuestionsManager import *
from sqlalchemy import exc, orm

class Test_create_question(unittest.TestCase):

	def setUp(self):
		self.QuestionManager = create_question()
	
	''' test - add no question '''
	
	def test_type_no_questions(self):
		with self.assetRaises(TypeError):
			self.QuestionManager.create_question('0')

	''' test - successfully add optional question '''
	
	def test_successfully_type_question1(self):
		self.QuestionsManager.create_question(datapacket, 1, 'test1', 'boolean', 'Optional')
		self.asserEqual(question_type, 'boolean')
		self.assertEqual(question_state, 'Optional')
		
	''' test - successfully add mandatory question '''
	
	def test_successfully_type_question2(self):
		self.QuestionsManager.create_question(datapacket, 2, 'test2', 'boolean', 'Generic')	
		self.asserEqual(question_type, 'boolean')
		self.assertEqual(question_state, 'Generic')
