from ..app import app, db, login
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from  ..API_lol.data_account import ranking_information
from sqlalchemy import func


class AccountFollowed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(255))

    def ajout_account(username):
        erreurs = []
        user_id = current_user.id
        data = ranking_information(username)
        if not username:
            erreurs.append("There is no username")
        unique = len(AccountFollowed.query.with_entities(AccountFollowed.username).filter_by(user_id=current_user.id,username=username).all())
        if unique > 0:
            erreurs.append("You already follow the account :" + username)
        if not data:
            erreurs.append("Failed to retrieve data for this account:"+ username +", it could be that you used the wrong UserName")
        if len(erreurs) > 0:
            return False, erreurs

        data_add = DataRanking(
            tier= data[2],
            lp= data[3],
            summoner_name=data[0],
            rank=data[1],
            account_followed_id=user_id

        )
        new_account = AccountFollowed(
            username=username,
            user_id=user_id
        )

        try:
            db.session.add(data_add)
            db.session.add(new_account)
            db.session.commit()
            return True, erreurs
        except Exception as erreur:
            return False, [str(erreur)]

    def update_account(username):
        new_data = ranking_information(username)
        old_data_tuple = DataRanking.query.with_entities(DataRanking.summoner_name, DataRanking.rank, DataRanking.tier,DataRanking.lp).filter_by(account_followed_id=current_user.id,summoner_name=username).all()
        old_data = list(old_data_tuple[0])
        print(old_data,new_data)
        if old_data[1] != new_data[1] or old_data[2]!= new_data[2] or old_data[3]!= new_data[3]:
            DataRanking.query.filter(DataRanking.summoner_name==username).update({"lp": new_data[3]})
            DataRanking.query.filter(DataRanking.summoner_name == username).update({"tier": new_data[2]})
            DataRanking.query.filter(DataRanking.summoner_name == username).update({"rank": new_data[1]})
            db.session.commit()


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
