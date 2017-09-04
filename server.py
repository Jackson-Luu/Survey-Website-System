"""
    In this server.py, we will handle all of the server side issue
    with python
"""
from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"