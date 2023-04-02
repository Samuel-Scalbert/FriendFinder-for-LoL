from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
api_key = "RGAPI-eba82191-0a2f-4d15-a5e8-f792c659f821"
login = LoginManager(app)
login.login_view = "login"

from .routes import home, users, my_friends, test_choix_compte