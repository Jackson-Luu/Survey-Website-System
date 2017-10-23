''' test creating survey
	user story - 3 '''

import unittest
import os
from server import APP, LOGIN_MANAGER
from flask import session
from modules.head import *
from modules.Authenticate import *
from modules.DataPacket import *
from modules.SurveyManager import *
from sqlalchemy import exc, orm


class test_create_survey(unittest.TestCase):

    def setUp(self):
        self.TESTDB = DBManager("testdb")

    def test_create_survey(self):
        add_packet = DataPacket("test", QUESTION_COL_IDS, "_questions")
        add_packet.add_data([0, "In the jungle", "0", "0"])
        add_packet.add_data([1, "The mightly", "0", "0"])
        add_packet.add_data([2, "Jungle. The lion", "0", "0"])
        add_packet.add_data([3, "sleeps tonight", "0", "0"])
        add_packet.add_data([4, "IN THE JUNGLE", "0", "0"])
        self.TESTDB.add_data(add_packet)

        survey_packet = DataPacket("test", SURVEY_COL_IDS, "_surveys")
        create_survey(survey_packet, 0, "NULL", [0, 1, 2, 3, 4], "Review")
        create_survey(survey_packet, 1, "NULL", [0, 1], "Review")
        create_survey(survey_packet, 2, "NULL", [3, 4], "Review")
        self.TESTDB.add_data(survey_packet)

        read_survey_packet = DataPacket("test", SURVEY_COL_IDS, "_surveys")
        self.TESTDB.retrieve_data(read_survey_packet)

        actual = read_survey_packet.retrieve_data()
        expected = [
            ["0", "NULL", "0,1,2,3,4", "Review"],
            ["1", "NULL", "0,1", "Review"],
            ["2", "NULL", "3,4", "Review"]
        ]
        self.assertListEqual(actual, expected)

    def test_delete_survey(self):
        add_packet = DataPacket("test", QUESTION_COL_IDS, "_questions")
        add_packet.add_data([0, "In the jungle", "0", "0"])
        add_packet.add_data([1, "The mightly", "0", "0"])
        add_packet.add_data([2, "Jungle. The lion", "0", "0"])
        add_packet.add_data([3, "sleeps tonight", "0", "0"])
        add_packet.add_data([4, "IN THE JUNGLE", "0", "0"])
        self.TESTDB.add_data(add_packet)

        survey_packet = DataPacket("test", SURVEY_COL_IDS, "_surveys")
        create_survey(survey_packet, 0, "NULL", [0, 1, 2, 3, 4], "Review")
        create_survey(survey_packet, 1, "NULL", [0, 1], "Review")
        create_survey(survey_packet, 2, "NULL", [3, 4], "Review")
        self.TESTDB.add_data(survey_packet)

        delete_packet = DataPacket("test", ["ID"], "_surveys")
        delete_packet.add_data(["0"])
        self.TESTDB.remove_data(delete_packet)

        read_survey_packet = DataPacket("test", SURVEY_COL_IDS, "_surveys")
        self.TESTDB.retrieve_data(read_survey_packet)

        actual = read_survey_packet.retrieve_data()
        expected = [
            ["1", "NULL", "0,1", "Review"],
            ["2", "NULL", "3,4", "Review"]
        ]
        self.assertListEqual(actual, expected)
    
    def test_remove_question(self):
        add_packet = DataPacket("test", QUESTION_COL_IDS, "_questions")
        add_packet.add_data([0, "In the jungle", "0", "0"])
        add_packet.add_data([1, "The mightly", "0", "0"])
        add_packet.add_data([2, "Jungle. The lion", "0", "0"])
        add_packet.add_data([3, "sleeps tonight", "0", "0"])
        add_packet.add_data([4, "IN THE JUNGLE", "0", "0"])
        self.TESTDB.add_data(add_packet)

        survey_packet = DataPacket("test", SURVEY_COL_IDS, "_surveys")
        create_survey(survey_packet, 0, "NULL", [0, 1, 2, 3, 4], "Review")
        create_survey(survey_packet, 1, "NULL", [0, 1], "Review")
        create_survey(survey_packet, 2, "NULL", [3, 4], "Review")
        self.TESTDB.add_data(survey_packet)

        delete_packet = DataPacket("test", ["ID"], "_questions")
        delete_packet.add_data(["0"])
        self.TESTDB.remove_data(delete_packet)

        read_survey_packet = DataPacket("test", SURVEY_COL_IDS, "_surveys")
        self.TESTDB.retrieve_data(read_survey_packet)

        actual = read_survey_packet.retrieve_data()
        expected = [
            ["0", "NULL", "0,1,2,3,4", "Review"],
            ["1", "NULL", "0,1", "Review"],
            ["2", "NULL", "3,4", "Review"]
        ]
        self.assertListEqual(actual, expected)

    def tearDown(self):
        self.TESTDB.delete_self()

if __name__ == '__main__':
    unittest.main()