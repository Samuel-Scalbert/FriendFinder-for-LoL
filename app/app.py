from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
api_key = "RGAPI-ccedf9be-d967-4fba-b200-a09887cb94af"
login = LoginManager(app)
login.login_view = "login"

from .routes import home, users, my_friends, match_records, mastery