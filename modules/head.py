from enum import Enum
from flask import Flask, flash, redirect, render_template, request, url_for, Response
from flask_login import LoginManager,login_user, current_user, login_required, logout_user, UserMixin
from wtforms import Form, StringField, PasswordField, validators, TextField, SelectField, IntegerField, SubmitField

class QuestionType(Enum):
    """ This is is just to standarise the question types across the
        files.
    """
    TEXT = 0 # The question is text based
    BOOL = 1 # True or false question
    RATI = 2 # Rating based on numbers
    RATS = 3 # Rating based on text
