''' test authorisation
	user story - 2 '''

import unittest
import os
from Authenticate import *
from sqlalchemy import exc, orm

class Test_Authenticate(unittest.TestCase):

	def setUp(self):
		self.Authenticate = Authenticate()

	''' test - provide the wrong username '''

	def test_wrong_username(self):
		self.Authenticate.CheckCreds('3232432','staff670')        
		with self.assertRaises(exc.IntegrityError):
			self.Authenticate.CheckCreds('3232432','staff670')   

	''' test - provide the wrong password '''

	def test_wrong_password(self):
		self.Authenticate.CheckCreds('51','bhnbhb')        
		with self.assertRaises(exc.IntegrityError):
			self.Authenticate.CheckCreds('51','bhnbhb') 

	''' test - provide correct login credentials'''
      
	def test_successful_input(self):
		self.Authenticate.CheckCreds('52','staff342')
		role = self.Authenticate.CheckCreds('52', 'staff342')
		self.assertEqual(username, '52')
		self.assertEqual(password, 'staff342')
