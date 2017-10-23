import unittest
import os
from Authenticate import *
from sqlalchemy import exc, orm

class Test_Authenticate(unittest.TestCase):

  def setUp(self):
    self.Authenticate = Authenticate()

  def test_wrong_username(self):
    self.Authenticate.CheckCreds('wrongusername','student')        
    with self.assertRaises(exc.IntegrityError):
      self.Authenticate.CheckCreds('wrongusername','student')   
  
  def test_wrong_password(self):
    self.Authenticate.CheckCreds('staff670','wrongpassword')        
    with self.assertRaises(exc.IntegrityError):
      self.Authenticate.CheckCreds('staff670','wrongpassword) 
      
  def test_successful_input(self):
    self.Authenticate.CheckCreds('staff670','staff')
