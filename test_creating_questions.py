''' testing the creation of various types of questions
	user story - 6 & 7 '''
	
import unittest
import os
from modules.head import *
from modules.QuestionsManager import *
from sqlalchemy import exc, orm

class test_create_question(unittest.TestCase):

	def setUp(self):
		self.QuestionManager = create_question()
		
	''' test - creating a multiple choice question (boolean) '''
	
	def test_create_mcq1(self):
		self.QuestionManager.create_question(data_packet, '1', 'question', 'boolean', 'Generic')
		self.assertEqual(type_enum, 1)
	
	''' test - creating a multiple choice question (numeric rating) ''' 
	
	def test_create_mcq2(self):
		self.QuestionManager.create_question(data_packet, '2', 'question', 'rating_int', 'Generic')
		self.assertEqual(type_enum, 2)
		
	''' test - creating a multiple choice question (text rating) ''' 
	
	def test_create_mcq2(self):
		self.QuestionManager.create_question(data_packet, '3', 'question', 'rating_text', 'Generic')
		self.asserEqual(type_enum, 3)