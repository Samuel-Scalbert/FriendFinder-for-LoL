from flask import url_for, render_template, redirect, request, flash
from ..models.data_base import Users
from ..models.formulaires import AjoutUtilisateur, Connexion
from ..utils.transformations import clean_arg
from ..app import app
from flask_login import login_user, current_user,  logout_user
from  ..API_lol.API_check import API_check


@app.route("/user/create_a_new_account", methods=["GET", "POST"])
def add_new_user():
    form = AjoutUtilisateur()
    if form.validate_on_submit():
        statut, donnees = Users.ajout_user(
            username=clean_arg(request.form.get("username", None)),
            password=clean_arg(request.form.get("password", None))
        )
        if statut is True:
            flash("You created your new account", "success")
            return redirect(url_for("home"))
        else:
            flash(",".join(donnees), "info")
            return render_template("pages/ajout_user.html", form=form)
    else:
        return render_template("pages/ajout_user.html", form=form)

@app.route("/user/login", methods=["GET","POST"])
def login():
    form = Connexion()

    if current_user.is_authenticated is True:
        flash("You are already logged in", "success")
        return redirect(url_for("home"))

    if form.validate_on_submit():
        username = Users.identification(
            username=clean_arg(request.form.get("username", None)),
            password=clean_arg(request.form.get("password", None))
        )
        if username:
            flash("Welcome back! You are logged in", "success")
            login_user(username)
            if API_check() == True:
                flash('The API is working fine !', "success")
                return redirect(url_for("home"))
            else:
                flash('The API might be over flooded right now wait a minute please', "info")
            return redirect(url_for("home"))
        else:
            flash("Wrong username", "info")
            return render_template("pages/connexion.html", form=form)

    else:
        return render_template("pages/connexion.html", form=form)

login.login_view = 'connexion'

@app.route("/user/logout", methods=["POST", "GET"])
def logout():
    if current_user.is_authenticated is True:
        logout_user()
    flash("You have been loged out", "info")
    return redirect(url_for("home"))
