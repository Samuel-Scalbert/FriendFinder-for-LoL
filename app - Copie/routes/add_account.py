from flask import url_for, render_template, redirect, request, flash
from ..models.data_base import AccountFollowed, DataRanking, Users
from ..models.formulaires import AjoutUtilisateur, Connexion, NewFollower
from ..utils.transformations import clean_arg
from ..app import app, login, db
from flask_login import login_user, current_user,  logout_user, login_required
import requests
from ..app import api_key

@app.route('/add_account', methods=['GET', 'POST'])
@login_required
def add_account():
    form = NewFollower()
    if form.validate_on_submit():
        statut, donnees = AccountFollowed.ajout_account(username=clean_arg(request.form.get("username")))
        if statut is True:
            flash("Ajout effectué", "success")
            return redirect(url_for("home"))
        else:
            flash(",".join(donnees), "error")
            return render_template("pages/new_follower.html", form=form)
    else:
        return render_template("pages/new_follower.html", form=form)