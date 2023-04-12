from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
api_key = "RGAPI-7de3cbc8-44bf-4ad0-b0fe-fb56b16d7d4e"
login = LoginManager(app)
login.login_view = "login"

from .routes import home, users, my_friends, test_choix_compte, match_records