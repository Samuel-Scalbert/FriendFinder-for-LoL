from flask import url_for, render_template, redirect, request, flash
from ..models.data_base import Users
from ..models.formulaires import AjoutUtilisateur, Connexion
from ..utils.transformations import clean_arg
from ..app import app, login
from flask_login import login_user, current_user,  logout_user

@app.route("/user/ajout", methods=["GET", "POST"])
def ajout_user():
    form = AjoutUtilisateur()

    if form.validate_on_submit():
        statut, donnees = Users.ajout_user(
            username=clean_arg(request.form.get("username", None)),
            password=clean_arg(request.form.get("password", None))
        )
        if statut is True:
            flash("Ajout effectué", "success")
            return redirect(url_for("home"))
        else:
            flash(",".join(donnees), "error")
            return render_template("pages/ajout_user.html", form=form)
    else:
        return render_template("pages/ajout_user.html", form=form)

@app.route("/user/connexion", methods=["GET","POST"])
def connexion():
    form = Connexion()

    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté", "info")
        return redirect(url_for("accueil"))

    if form.validate_on_submit():
        username = Users.identification(
            username=clean_arg(request.form.get("username", None)),
            password=clean_arg(request.form.get("password", None))
        )
        if username:
            flash("Connexion effectuée", "success")
            login_user(username)
            return redirect(url_for("home"))
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")
            return render_template("pages/connexion.html", form=form)

    else:
        return render_template("pages/connexion.html", form=form)

login.login_view = 'connexion'

@app.route("/user/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("You have been loged out", "info")
    return redirect(url_for("home"))