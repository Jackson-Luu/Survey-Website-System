class admin:
    """Common class for all admins
       Attributes: name, username and password
       given at the time of registration.
    """
  
    #Constructor
    def __init__(self, name, username, password):
        self._name = name
        self._username = username
        self._password = password
