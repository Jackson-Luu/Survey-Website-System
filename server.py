from modules.head import *

APP = Flask(__name__)
APP.secret_key = 'Secret'

LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(APP)
