import unittest
import os
from QuestionsManager import *
from sqlalchemy import exc, orm

class Test_create_question(unittest.TestCase):

	def test_type_no_questions(self):
		with self.assetRaises(TypeError):
			self.QuestionManager.create_question('0')

	def test_successfully_type_question(self):
		self.QuestionsManager.create_question("""datapacket""", '1', 'test1', 'boolean', 'admin')
		self.asserEqual(user_type, 'admin')
		self.asserEqual(question_type, 'boolean')
		
		
		

