from ..app import app, login
from flask import url_for, render_template, redirect, flash

# The following function is decorated by the `@app` route decorators,
# which specifies the URL paths that should trigger this function when accessed.
@app.route("/")
@app.route("/home")
def home():
    # This function returns the rendered template file `home.html` present in the `pages` folder.
    return render_template("pages/home.html")

# This function is decorated by the `@login` decorator with the `unauthorized_handler` argument.
# It handles unauthorized access by flashing a message to the user and redirecting them to the home page.
def unauthorized():
    flash("You need to login to access this page", "info")
    return redirect(url_for("home"))