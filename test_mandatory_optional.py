''' testing the creation of optional and mandatory questions 
	user story - 4 '''

import unittest
import os
from server import APP, LOGIN_MANAGER 
from flask import session 
from modules.head import *
from modules.Authenticate imprt *
from modules.DataPacket import *
from sqlalchemy import exc, orm

class Test_create_question(unittest.TestCase):

	def setUp(self):
		self.TestDB = DBManager("testdb")
	
	def test_optional_questions(self):
		add_packet = DataPacket("test", QUESTION_GEN_OPT, "_questions")
		add_packet.add_data([4, "test 1", "0", "OPTIONAL"])
		add_packet.add_data([5, "test 2", "0", "OPTIONAL"])
		add_packet.add_data([6, "test 3", "0", "OPTIONAL"])
		add_packet.add_data([7, "test 4", "0", "OPTIONAL"])
		self.TESTDB.add_data(retrieve_packet)
		
		retrieve_packet = DataPacket("test", QUESTION_GEN_OPT, "_questions")
		self.TESTDB.retrieve_data(retrieve_packet)
		
		actual = retrieve_packet.retrieve_data()
        	expected = [
            		[4, "test 1", "0", "Optional"],
            		[5, "test 2", "0", "Optional"],
            		[6, "test 3", "0", "Optional"],
            		[7, "test 4", "0", "Optional"]
       		]
       		
		self.assertListEqual(actual, expected)		
		
	def test_generic_questions(self):
		add_packet = DataPacket("test", QUESTION_GEN_OPT, "_questions")
		add_packet.add_data([8, "test 5", "0", "Generic"])
		add_packet.add_data([9, "test 6", "0", "Generic"])
		add_packet.add_data([10, "test 7", "0", "Generic"])
		add_packet.add_data([11, "test 8", "0", "Generic"])
		self.TESTDB.add_data(retrieve_packet)
		
		retrieve_packet = DataPacket("test", QUESTION_GEN_OPT, "_questions")
		self.TESTDB.retrieve_data(retrieve_packet)
		
		actual = retrieve_packet.retrieve_data()
        	expected = [
            		[8, "test 5", "0", "Generic"],
            		[9, "test 6", "0", "Generic"],
            		[10, "test 7", "0", "Generic"],
            		[11, "test 8", "0", "Generic"]
       		]
       		
		self.assertListEqual(actual, expected)	
		
	@unittest.expectedOPTfailure
	
	def test_optional_questions_fail(self):
		add_packet = DataPacket("test", QUESTION_GEN_OPT, "_questions")
		add_packet.add_data([4, "test 1", "0", "Optional"])
		add_packet.add_data([4, "test 1", "0", "Optional"])
		add_packet.add_data([5, "test 2", "0"])
		add_packet.add_data([6, "test 3", 0, Optional])
		self.TESTDB.add_data(add_packet) 
		
	def tearDown(self):
        	self.TESTDB.delete_self()			
		
	@unittest.expectedGENfailure
	
	def test_generic_questions_fail(self):
		add_packet = DataPacket("test", QUESTION_GEN_OPT, "_questions")
		add_packet.add_data([8, "test 5", "0", "Generic"])
		add_packet.add_data([8, "test 5", "0", "Generic"])
		add_packet.add_data([9, "test 6", "0"])
		add_packet.add_data([10, "test 7", 0, Generic])
		self.TESTDB.add_data(add_packet) 
		
	def tearDown(self):
        	self.TESTDB.delete_self()				

if __name__ == '__main__':
	unittest.main()

