''' test authorisation
	user story - 2 '''

import unittest
import os
from modules.Authenticate import *
from sqlalchemy import exc, orm


class Test_Authenticate(unittest.TestCase):
    def test_correct(self):
        self.assertTrue(Authenticate("admin", "password"))
        self.assertTrue(Authenticate("50", "staff670"))
        self.assertTrue(Authenticate("51", "staff462"))
        self.assertTrue(Authenticate("52", "staff342"))
        self.assertTrue(Authenticate("53", "staff244"))
        self.assertTrue(Authenticate("100", "student228"))
        self.assertTrue(Authenticate("101", "student756"))
        self.assertTrue(Authenticate("102", "student627"))
        self.assertTrue(Authenticate("103", "student711"))
        self.assertTrue(Authenticate("132", "student765"))
        self.assertTrue(Authenticate("1029", "staff1029"))
        self.assertTrue(Authenticate("1030", "staff1030"))
        self.assertTrue(Authenticate("1031", "staff1031"))
    
    def test_incorrect(self):
        self.assertFalse(Authenticate("admin", "d"))
        self.assertFalse(Authenticate("50", "dsf"))
        self.assertFalse(Authenticate("51", "sdfasd"))
        self.assertFalse(Authenticate("52", "staffds342"))
        self.assertFalse(Authenticate("53", "staff2d44"))
        self.assertFalse(Authenticate("100", "dsfa"))
        self.assertFalse(Authenticate("101", "studdsfsdfent756"))
        self.assertFalse(Authenticate("102", "sdfdsfsda"))
        self.assertFalse(Authenticate("103", "studensdt711"))
        self.assertFalse(Authenticate("132", "studesdfnt765"))
        self.assertFalse(Authenticate("1029", "staff10sdf29"))
        self.assertFalse(Authenticate("1030", "staff1sdf030"))
        self.assertFalse(Authenticate("1031", "staff1dsf031"))

if __name__ == '__main__':
    unittest.main()