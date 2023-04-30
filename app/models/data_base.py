from ..app import app, db, login
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from  ..API_lol.data_account import ranking_information
from  ..API_lol.LP_gains import LP_Gains


# Define a class called AccountFollowed
class AccountFollowed(db.Model):
    # Create a column called "id" that is an integer and primary key
    id = db.Column(db.Integer, primary_key=True)
    # Create a column called "user_id" that is an integer and foreign key to the 'users' table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Create a column called "username" that is a string of maximum length 255 characters
    username = db.Column(db.String(255))

    # Define a function called "ajout_account" that takes a username parameter
    def ajout_account(username):
        # Create an empty list to store any errors that occur
        erreurs = []
        # Get the current user's id and store it in a variable called "user_id"
        user_id = current_user.id
        # Get the ranking information for the given username and store it in a variable called "data"
        data = ranking_information(username)
        # If no username is provided, add an error message to the "erreurs" list
        if not username:
            erreurs.append("There is no username")
        # Check if the user already follows the given account, and add an error message if they do
        unique = len(AccountFollowed.query.with_entities(AccountFollowed.username).filter_by(user_id=current_user.id,username=username).all())
        if unique > 0:
            erreurs.append("You already follow the account :" + username)
        # If no data is retrieved for the given account, add an error message to the "erreurs" list
        if not data:
            erreurs.append("Failed to retrieve data for this account:"+ username +", it could be that you used the wrong UserName")
        # If there are any errors, return False and the "erreurs" list
        if len(erreurs) > 0:
            return False, erreurs

        # Create a new DataRanking object with the retrieved data
        data_add = DataRanking(
            tier= data[2],
            lp= data[3],
            summoner_name=data[0],
            rank=data[1],
            account_followed_id=user_id

        )
        # Create a new AccountFollowed object with the given username and the current user's id
        new_account = AccountFollowed(
            username=username,
            user_id=user_id
        )

        # Try to add the new data and new account to the database, and return True if successful or False and an error message if not
        try:
            db.session.add(data_add)
            db.session.add(new_account)
            db.session.commit()
            return True, erreurs
        except Exception as erreur:
            return False, [str(erreur)]

    # Define a function that takes a username parameter and updates account information
    def update_account(username):
        # Call a function to retrieve new ranking information for the given username
        new_data = ranking_information(username)

        # Retrieve old ranking information from the database for the given username
        # and current user's account ID
        old_data_tuple = DataRanking.query.with_entities(DataRanking.summoner_name, DataRanking.rank, DataRanking.tier,
                                                         DataRanking.lp).filter_by(account_followed_id=current_user.id,
                                                                                   summoner_name=username).all()

        # Convert the tuple of old ranking information to a list
        old_data = list(old_data_tuple[0])

        # Check if any of the old ranking data is different from the new data
        if old_data[1] != new_data[1] or old_data[2] != new_data[2] or old_data[3] != new_data[3]:
            # Calculate the difference in league points between the old and new data
            league_points = LP_Gains(old_data, new_data)

            # Update the database with the new league points difference
            DataRanking.query.filter(DataRanking.summoner_name == username).update({"lp_diff": league_points})

            # Update the database with the new league points for the given username
            DataRanking.query.filter(DataRanking.summoner_name == username).update({"lp": new_data[3]})

            # Update the database with the new tier for the given username
            DataRanking.query.filter(DataRanking.summoner_name == username).update({"tier": new_data[2]})

            # Update the database with the new rank for the given username
            DataRanking.query.filter(DataRanking.summoner_name == username).update({"rank": new_data[1]})

            # Commit the changes to the database
            db.session.commit()

# Defining a class called DataRanking, which is a subclass of db.Model
class DataRanking(db.Model):
    # Defining class variables as columns in the table
    # 'id' is a primary key, which is a unique identifier for each record
    id = db.Column(db.Integer, primary_key=True)
    # 'tier' is an integer column to store the tier of the summoner
    tier = db.Column(db.Integer)
    # 'lp' is an integer column to store the league points of the summoner
    lp = db.Column(db.Integer)
    # 'summoner_name' is a string column to store the name of the summoner, and it cannot be null
    summoner_name = db.Column(db.String(255), nullable=False)
    # 'rank' is a string column to store the rank of the summoner
    rank = db.Column(db.String(255))
    # 'account_followed_id' is an integer column that references the primary key of another table called 'account_followed'
    account_followed_id = db.Column(db.Integer, db.ForeignKey('account_followed.id'))
    # 'lp_diff' is an integer column to store the difference in league points from the last update
    lp_diff = db.Column(db.Integer)

    # Defining a string representation of the class instance
    def __repr__(self):
        return f"DataRanking(id={self.id}, summoner_name='{self.summoner_name}')"


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    accounts_followed = db.relationship('AccountFollowed', backref='following_users', lazy=True)

    def ajout_user(username, password):
        erreurs = []
        if not username:
            erreurs.append("Le username est vide")
        if not password or len(password) < 6:
            erreurs.append("Le mot de passe est vide ou trop court")

        unique = Users.query.filter(
            db.or_(Users.username == username)
        ).count()
        if unique > 0:
            erreurs.append("Le username existe déjà")

        if len(erreurs) > 0:
            return False, erreurs

        username = Users(
            username=username,
            password=generate_password_hash(password)
        )

        try:
            db.session.add(username)
            db.session.commit()
            return True, username
        except Exception as erreur:
            return False, [str(erreur)]

    def get_id(self):
        return self.id

    @staticmethod
    def identification(username, password):
        utilisateur = Users.query.filter(Users.username == username).first()
        if utilisateur and check_password_hash(utilisateur.password, password):
            return utilisateur
        return None


    @login.user_loader
    def get_user_by_id(id):
        return Users.query.get(int(id))
