from ..app import app, login
from flask import url_for, render_template, redirect, flash



@app.route("/")
@app.route("/home")
def home():
    return render_template("pages/home.html")

@login.unauthorized_handler
def unauthorized():
    flash("You need to login to access this page", "info")
    return redirect(url_for("home"))