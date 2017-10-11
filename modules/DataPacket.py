""" File used to write out the data packet """

class DataPacket():
    """ The data packet is to store all of the information into a standarised
        format that can be used by Database Manager to store the information
        into the database.

        query_ids denote the title given to the information when stored into
        the database.
    """

    def __init__(self, user_id, query_ids, suffix=""):
        if isinstance(query_ids, list):
            self._query_ids = query_ids
            self._query_num = len(query_ids)

            self._user_id = user_id  # To denote who owns this packet
            self._query_data = []    # Used to store all of the data
            self._suffix = suffix
        else:
            raise Exception('query_ids Must be of type list')

    def add_data(self, data):
        """ Add a list of data of the appropriate length to the packet """

        if len(data) != self._query_num:
            print("Rejected data packet")
            return

        # Force convert all of the data into a str to be safe
        final_data = [str(d) for d in data]

        self._query_data.append(final_data)

    def set_suffix(self, suffix):
        self._suffix = suffix

    def retrieve_suffix(self):
        return self._suffix

    def retrieve_user_id(self):
        """ Retrieves the owner's id """
        return self._user_id

    def retrieve_query_id(self):
        """ Retrieve the query_ids """
        return self._query_ids

    def retrieve_query_num(self):
        """ Retrieve the number of query_ids """
        return self._query_num

    def retrieve_data(self):
        """ Retrieve the data """
        return self._query_data
