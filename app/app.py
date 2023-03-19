from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)

db = SQLAlchemy(app)
api_key = "RGAPI-b2136b80-3a07-4733-be69-d5cfc5cc646f"
login = LoginManager(app)

from .routes import generales, users, my_account