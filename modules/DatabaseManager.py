""" 
    The purpose of the database manager is to delegate all of the accessing of data
    to a single class. In doing this, we are able to change how we access the database without
    causing much issue.
"""
import os
import sqlite3
from modules.DataPacket import DataPacket
from modules.head import *

class DBManager():
    """ The class that will create a database manager """
    def __init__(self, file_name):
        self._file_name = file_name
        # Change the file extension if you want to change how the data is stored
        self._file_ext = '.db'
        self._final_path = 'storage/' + self._file_name + self._file_ext

    def db_query(self, query, args):
        """ function to execute database queries """
        connection = sqlite3.connect(self._final_path)
        cursorObj = connection.cursor()

        if not args:
            result = cursorObj.execute(query)
        else:
            args = tuple(args)
            result = cursorObj.execute(query, args)
        connection.commit()

        rows = []
        if result:
            for row in result:
                rows.append(row)
        cursorObj.close()
        return rows

    def prepare_create_query_str(self, data_packet):
        """ Prepare a query string to add a new table if needed """
        user = data_packet.retrieve_user_id()
        query = 'CREATE TABLE IF NOT EXISTS "{}" ('

        first_run = True
        for query_id in data_packet.retrieve_query_id():
            if first_run:
                query = query + '{} TEXT PRIMARY KEY NOT NULL'.format(query_id)
                first_run = False
            else:
                query = query + ',{} TEXT NOT NULL'.format(query_id)

        query = query + ');'
        query = query.format(user)
        return query

    def prepare_query_str(self, data_packet):
        """ Prepare a query string to add data to the table """

        user = data_packet.retrieve_user_id()
        query = 'INSERT INTO "{}" ('
        first_run = True

        # We are just going to write the query ids to the query string
        for query_id in data_packet.retrieve_query_id():
            if first_run:
                query = query + query_id
                first_run = False
            else:
                query = query + ',' + query_id

        query = query + ') VALUES ('

        first_run = True
        # Write the ? into the query string
        for x in range(0, data_packet.retrieve_query_num()):
            if first_run:
                query = query + '?'
                first_run = False
            else:
                query = query + ',?'

        query = query + ');'
        query = query.format(user)

        return query

    def retrieve_data(self, data_packet):
        """ Here, we are going to access the data and return it as a list """
        if not isinstance(data_packet, DataPacket):
            raise Exception("data_packet is not of type DataPacket")

        if os.path.exists(self._final_path):
            # If the file exists, open it and read the row of data
            user = data_packet.retrieve_user_id()

            # create new table for current user if it doesn't already exist
            query = self.prepare_create_query_str(data_packet)
            self.db_query(query, False)

            # read all from table
            query = 'SELECT * FROM "{}";'.format(user)
            for row in self.db_query(query, False):
                data_packet.add_data(row)
        else:
            open(self._final_path, 'w').close()
        return data_packet

    def add_data(self, data_packet):
        """ Here, we are going to add a question to the database """

        # if a valid question has been provided
        if isinstance(data_packet, DataPacket):
            # If the file exists, open it and read the row of data
            # create new table for current user if it doesn't already exist
            query = self.prepare_create_query_str(data_packet)
            self.db_query(query, False)

            # add question
            query = self.prepare_query_str(data_packet)
            for data in data_packet.retrieve_data():
                self.db_query(query, data)
        else:
            raise Exception("question given is not of type Question")

    def remove_data(self, delete_packet):
        """ Delete the data from the database """
        query_ids = delete_packet.retrieve_query_id()
        user = delete_packet.retrieve_user_id()

        for d in delete_packet.retrieve_data():
            first_run = True
            query = 'DELETE FROM "{}" WHERE ('

            for x in range(0, len(query_ids)):
                if first_run:
                    query = query + query_ids[x] + ' = ' + d[x]
                    first_run = False
                else:
                    query = query + ' AND ' + query_ids[x] + ' = ' + d[x]

            query = query + ')'
            query = query.format(user)
            self.db_query(query, None)

"""
    def modify_data(self, question):
            Modify the question in the database
        if isinstance(question, Question):
            listofquestion = []

            if os.path.exists(self._final_path):
                with open(self._final_path) as csvfile:
                    questionreader = csv.reader(csvfile)
                    for row in questionreader:
                        if row[0] != question.get_id():
                            listofquestion.append(row)
                        else:
                            listofquestion.append([question.get_id(), question.get_text(),
                                                   question.get_type().value])

            if len(listofquestion) != 0:
                with open(self._final_path, 'w') as csvfile:
                    for row in listofquestion:
                        questionwriter = csv.writer(csvfile)
                        questionwriter.writerow(row)
        else:
            raise Exception("question given is not of type Question")

    def retrieve_specific(self, question_id_list):
         Retrieve a specific list of Questions based on the question id
            listed
        

        if os.path.exists(self._final_path):
            # If the file exists, open it and read the row of data
            with open(self._final_path) as csvfile:
                listofquestion = []
                questionreader = csv.reader(csvfile)

                for row in questionreader:
                    if row[0] in question_id_list:
                        new_q = Question(row[0])

                        new_q.set_text(row[1])
                        new_q.set_type(QuestionType(int(row[2])))

                        listofquestion.append(new_q)

            return listofquestion
        else:
            open(self._final_path, 'w').close()
            return []
"""