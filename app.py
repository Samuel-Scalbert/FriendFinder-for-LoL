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
api_key = "RGAPI-b5ee5978-66cc-45b2-b10c-07a4889b46d8"
login = LoginManager(app)

from .routes import generales, users, add_account, mastery, match_records