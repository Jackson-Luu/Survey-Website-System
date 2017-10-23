''' testing the creation of various types of questions
	user story - 6 & 7 '''

import unittest
import os
from server import APP, LOGIN_MANAGER
from flask import session
from modules.head import *
from modules.Authenticate import *
from modules.DataPacket import *
from sqlalchemy import exc, orm


class test_create_question(unittest.TestCase):

    def setUp(self):
        self.TESTDB = DBManager("testdb")

    def test_add_question(self):
        add_packet = DataPacket("test", QUESTION_COL_IDS, "_questions")
        add_packet.add_data([0, "Hello my honey", "0", "0"])
        add_packet.add_data([1, "Hello my honey", "0", "0"])
        add_packet.add_data([2, "Hello my honey", "0", "0"])
        add_packet.add_data([3, "Hello my honey", "0", "0"])

    def test_add_fail_questions(self):
        add_packet = DataPacket("test", QUESTION_COL_IDS, "_questions")
        add_packet.add_data([0, "Hello my honey", "0", "0"])
        add_packet.add_data([0, "Hello my honey", "0", "0"])
        add_packet.add_data([2, "Hello my honey", "0"])
        add_packet.add_data([3, "Hello my honey", 0, 0])

if __name__ == '__main__':
    unittest.main()
