from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
api_key = "RGAPI-7f91e36e-f315-4560-aee7-ec9ae070965a"
login = LoginManager(app)
login.login_view = "login"

from .routes import generales, users, my_account