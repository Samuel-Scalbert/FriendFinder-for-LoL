from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
api_key = "RGAPI-821239eb-7e1a-408b-b850-a96c8cd47d1c"
login = LoginManager(app)
login.login_view = "login"

from .routes import home, users, my_friends