from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import re

class AjoutUtilisateur(FlaskForm):
    username = StringField("username", validators=[])
    password = PasswordField("password", validators=[])

class Connexion(FlaskForm):
    username = StringField("username", validators=[])
    password = PasswordField("password", validators=[])

class NewFollower(FlaskForm):
    username = StringField("username", validators=[])