from flask import Flask, flash, redirect, render_template, request, url_for, Response
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from wtforms import Form, StringField, PasswordField, validators
