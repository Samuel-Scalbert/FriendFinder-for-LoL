from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
api_key = "RGAPI-fcffc66a-16d8-49d7-9f59-cf6da8b7ed97"
login = LoginManager(app)
login.login_view = "login"

from .routes import generales, users, my_account