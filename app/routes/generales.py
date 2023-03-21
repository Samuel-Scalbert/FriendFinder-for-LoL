from ..app import app, db, api_key, login
from flask import url_for, render_template, redirect, request, flash
from sqlalchemy import or_
from ..models.data_base import Users
from  ..API_lol.data_account import ranking_information


@app.route("/")
@app.route("/home")
def home():
    return render_template("pages/home.html")

@login.unauthorized_handler
def unauthorized():
    flash("You need to login to access this page", "info")
    return redirect(url_for("home"))