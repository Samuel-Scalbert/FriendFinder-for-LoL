from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
api_key = "RGAPI-7c178fe5-2791-459a-a50d-d0476caf72f2"
login = LoginManager(app)
login.login_view = "login"

from .routes import home, users, my_friends