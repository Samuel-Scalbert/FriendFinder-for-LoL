from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='statics')
app.config.from_object(Config)

db = SQLAlchemy(app)
api_key = "RGAPI-30726939-4ebb-483f-9522-e6824a3ca142"
login = LoginManager(app)

from .routes import generales, users, add_account, mastery, match_records