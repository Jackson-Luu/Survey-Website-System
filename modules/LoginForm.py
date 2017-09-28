from modules.head import *

class LoginForm(Form):
    username = StringField('Username', [validators.Length(max=40)])
    password = PasswordField('Password')
