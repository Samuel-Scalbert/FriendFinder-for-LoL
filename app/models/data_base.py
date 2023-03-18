from ..app import app, db, login
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from  ..API_lol.data_account import ranking_information

class AccountFollowed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(255))

    def ajout_account(username):
        erreurs = []
        user_id = current_user.id
        data = ranking_information([username])
        print(data)
        if not username:
            erreurs.append("There is no username")
        unique = AccountFollowed.query.filter(AccountFollowed.username == username).count()
        if unique > 0:
            erreurs.append("You already follow this account")
        if not data:
            print(data)
            erreurs.append("Failed to retrieve data for this account, it could be that you used the wrong UserName")
        if len(erreurs) > 0:
            return False, erreurs

        new_account = AccountFollowed(
            username=username, user_id=user_id
        )

        try:
            db.session.add(new_account)
            db.session.commit()
            return True, erreurs
        except Exception as erreur:
            return False, [str(erreur)]


class DataRanking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tier = db.Column(db.Integer)
    lp = db.Column(db.Integer)
    summoner_name = db.Column(db.String(255), nullable=False)
    rank = db.Column(db.String(255))
    account_followed_id = db.Column(db.Integer, db.ForeignKey('account_followed.id'))

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
