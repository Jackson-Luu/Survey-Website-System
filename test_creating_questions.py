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
        self.TESTDB = DBManager("testdb", True)

    def test_add_question(self):
        add_packet = DataPacket("test", QUESTION_COL_IDS, "_questions")
        add_packet.add_data([0, "Hello my honey", "0", "0"])
        add_packet.add_data([1, "Hello my honey", "0", "0"])
        add_packet.add_data([2, "Hello my honey", "0", "0"])
        add_packet.add_data([3, "Hello my honey", "0", "0"])
        self.TESTDB.add_data(add_packet)

        retrieve_packet = DataPacket("test", QUESTION_COL_IDS, "_questions")
        self.TESTDB.retrieve_data(retrieve_packet)

        actual = retrieve_packet.retrieve_data()
        expected = [
            ['0', "Hello my honey", "0", "0"],
            ['1', "Hello my honey", "0", "0"],
            ['2', "Hello my honey", "0", "0"],
            ['3', "Hello my honey", "0", "0"]
        ]
        self.assertListEqual(actual, expected)

    @unittest.expectedFailure
    def test_add_fail_questions(self):
        add_packet = DataPacket("test", QUESTION_COL_IDS, "_questions")
        add_packet.add_data([0, "Hello my honey", "0", "0"])
        add_packet.add_data([0, "Hello my honey", "0", "0"])
        add_packet.add_data([2, "Hello my honey", "0"])
        add_packet.add_data([3, "Hello my honey", 0, 0])
        self.TESTDB.add_data(add_packet)

    def tearDown(self):
        self.TESTDB.delete_self()

if __name__ == '__main__':
    unittest.main()
