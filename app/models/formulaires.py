from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, PasswordField
from ..models.data_base import AccountFollowed

# Defining a FlaskForm for adding a new user
class AjoutUtilisateur(FlaskForm):
    # Defining a StringField for the username field
    username = StringField("username", validators=[])
    # Defining a PasswordField for the password field
    password = PasswordField("password", validators=[])

# Defining a FlaskForm for user authentication
class Connexion(FlaskForm):
    # Defining a StringField for the username field
    username = StringField("username", validators=[])
    # Defining a PasswordField for the password field
    password = PasswordField("password", validators=[])

# Defining a FlaskForm for adding a new follower
class NewFollower(FlaskForm):
    # Defining a StringField for the username field
    username = StringField("username", validators=[])

# Defining a FlaskForm for choosing an account from a list of accounts associated with a user
class ChooseAccount(FlaskForm):
    # Defining a SelectField for selecting an account
    account = SelectField('Account', coerce=int)

    # Constructor to populate the account choices with accounts associated with the given user_id
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        # Setting the account choices to the list of (account.id, account.username) pairs for all accounts associated with the user_id
        self.account.choices = [(account.id, account.username) for account in AccountFollowed.query.filter_by(user_id=user_id).all()]

# Defining a FlaskForm for finding a match by puuid
class MatchFinder(FlaskForm):
    # Defining a StringField for the puuid field
    puuid = StringField("puuid", validators=[])