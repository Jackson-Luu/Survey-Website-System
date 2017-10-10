import csv
from modules.head import *

class UserClass(UserMixin):
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def get_role(self):
        return self.role

    def get_id(self):
        return str(self.username)

def CheckDatabase():
    user_packet = DataPacket("users", USER_COL_IDS, "")
    user_packet = DBMANAGER.retrieve_data(user_packet)

    if len(user_packet.retrieve_data()) == 0:
        with open('storage/passwords.csv') as csvfile:
            credreader = csv.reader(csvfile)
            for row in credreader:
                user_packet.add_data(row)

        DBMANAGER.add_data(user_packet)

def Authenticate(username, password):
    role = CheckCreds(username, password)
    if role != 'INVALID':
        newuser = UserClass(username, role)
        login_user(newuser)
        return True
    return False

def RestoreUser(username):
    with open('storage/passwords.csv') as csvfile:
        credreader = csv.reader(csvfile)
        for row in credreader:
            if username == row[0]:
                return UserClass(username, row[2])
    return None

def CheckCreds(username, password):
    CheckDatabase()
    user_packet = DataPacket("users", USER_COL_IDS, "")
    user_packet = DBMANAGER.retrieve_data(user_packet)

    for row in user_packet.retrieve_data():
        if username == row[0]:
            if password == row[1]:
                flash("You have successfully logged in")
                return row[2]

    flash("Invalid username or password")
    return "INVALID"
