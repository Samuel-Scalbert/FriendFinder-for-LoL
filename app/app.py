from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
api_key = "RGAPI-7e36ccb2-dce6-40a1-9c60-d3af41df3821"
login = LoginManager(app)
login.login_view = "login"

from .routes import home, users, my_friends, test_choix_compte