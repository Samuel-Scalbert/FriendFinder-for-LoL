from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
api_key = "RGAPI-1d9435f9-62f2-45f2-9e6b-07991ce1c250"
login = LoginManager(app)
login.login_view = "login"

from .routes import generales, users, my_account