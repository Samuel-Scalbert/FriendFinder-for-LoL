from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, PasswordField
from ..models.data_base import AccountFollowed

class AjoutUtilisateur(FlaskForm):
    username = StringField("username", validators=[])
    password = PasswordField("password", validators=[])

class Connexion(FlaskForm):
    username = StringField("username", validators=[])
    password = PasswordField("password", validators=[])

class NewFollower(FlaskForm):
    username = StringField("username", validators=[])

class ChooseAccount(FlaskForm):
    account = SelectField('Account', coerce=int)

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        self.account.choices = [(account.id, account.username) for account in AccountFollowed.query.filter_by(user_id=user_id).all()]

class MatchFinder(FlaskForm):
    puuid = StringField("puuid", validators=[])