from flask import url_for, render_template, redirect, request, flash
from ..models.data_base import Users, AccountFollowed
from ..models.formulaires import AjoutUtilisateur, Connexion, NewFollower
from ..utils.transformations import clean_arg
from ..app import app, login
from flask_login import login_user, current_user,  logout_user, login_required

@app.route('/my_account/add_account', methods=['GET', 'POST'])
@login_required
def add_account():
    form = NewFollower()
    if form.validate_on_submit():
        statut, donnees = AccountFollowed.ajout_account(username=clean_arg(request.form.get("username")))
        if statut is True:
            flash("Ajout effectué", "success")
            return redirect(url_for("add_account"))
        else:
            flash(",".join(donnees), "info")
            return render_template("pages/new_follower.html", form=form)
    else:
        return render_template("pages/new_follower.html", form=form)

@app.route('/my_account/my_friends', methods=['GET'])
@login_required
def my_friends():
    friends = AccountFollowed.query.with_entities(AccountFollowed.username).filter_by(user_id=current_user.id).all()
    usernames = [f[0] for f in friends]
    return render_template("pages/my_friends.html", usernames=usernames)

