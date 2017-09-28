from modules.head import *
import csv

def CheckCreds(username, password):
    with open('storage/passwords.csv') as csvfile:
        credreader = csv.reader(csvfile)
        for row in credreader:
            if username == row[0]:
                if password == row[1]:
                    return row[2]
        return "INVALID"
    return "INVALID"
