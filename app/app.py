from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)

db = SQLAlchemy(app)
api_key = "RGAPI-8a97ab11-b07a-403e-b6f5-5a6a3487b090"
login = LoginManager(app)
login.login_view = "login"

from .routes import generales, users, my_account