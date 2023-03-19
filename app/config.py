import dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config():
    DEBUG = os.environ.get("DEBUG")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO=os.environ.get("SQLALCHEMY_ECHO")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    WTF_CSRF_ENABLE = os.environ.get("WTF_CSRF_ENABLE")
    api_key = os.environ.get("RGAPI-733512e4-d53d-41d0-9e72-0effd967f013")