from flask import url_for, render_template, redirect, request, flash
from ..models.data_base import Users
from ..models.formulaires import AjoutUtilisateur, Connexion, MatchFinder
from ..utils.transformations import clean_arg
import requests
from ..app import app
from flask_login import login_user, current_user,  logout_user, login_required
from  ..API_lol.API_check import API_check


# This line defines a route in the Flask application that is triggered when a user navigates to "/user/create_a_new_account"
@app.route("/user/create_a_new_account", methods=["GET", "POST"])

# This function handles the request and response for the above route
def add_new_user():

    # This line creates a new instance of a form object called "AjoutUtilisateur"
    form = AjoutUtilisateur()

    # This block of code executes if the form has been submitted and validated successfully
    if form.validate_on_submit():

        # This line calls the method "ajout_user" of the "Users" class and passes the username and password data from the form
        # The data is cleaned using the "clean_arg" function before being passed to the method
        statut, donnees = Users.ajout_user(
            username=clean_arg(request.form.get("username", None)),
            password=clean_arg(request.form.get("password", None))
        )

        # This block of code executes if a new user is successfully added to the database
        if statut is True:

            # This line adds a message to the Flask message queue indicating that the user has successfully created a new account
            flash("You created your new account", "success")

            # This line redirects the user to the home page
            return redirect(url_for("home"))

        # This block of code executes if a new user is not successfully added to the database
        else:

            # This line adds a message to the Flask message queue indicating that the user was not able to create a new account
            # The error messages returned from the "ajout_user" method are joined together into a single string and displayed as the message
            flash(",".join(donnees), "info")

            # This line renders the "ajout_user.html" template with the form object passed as an argument
            return render_template("pages/ajout_user.html", form=form)

    # This block of code executes if the form has not been submitted or has not been validated successfully
    else:

        # This line renders the "ajout_user.html" template with the form object passed as an argument
        return render_template("pages/ajout_user.html", form=form)


# This code defines a route for user login
@app.route("/user/login", methods=["GET", "POST"])
def login():
    # A form object of the Connexion class is created
    form = Connexion()

    # Check if the user is already authenticated and redirect to home page if true
    if current_user.is_authenticated is True:
        flash("You are already logged in", "success")
        return redirect(url_for("home"))

    # Check if the form is validated on submit
    if form.validate_on_submit():

        # Call the identification method of the Users class to get the username
        # Clean the username and password input from the request form
        username = Users.identification(
            username=clean_arg(request.form.get("username", None)),
            password=clean_arg(request.form.get("password", None))
        )

        # If the username exists, log in the user and redirect to home page
        if username:
            flash("Welcome back! You are logged in", "success")
            login_user(username)

            # Check if the API is working and display success message
            if API_check() == True:
                flash('The API is working fine !', "success")
                return redirect(url_for("home"))
            # If API is not working, display info message and redirect to home page
            else:
                flash('The API might be over flooded right now wait a minute please', "info")
            return redirect(url_for("home"))

        # If the username is incorrect, display info message and render the login page again
        else:
            flash("Wrong username", "info")
            return render_template("pages/connexion.html", form=form)

    # If the form is not validated, render the login page again
    else:
        return render_template("pages/connexion.html", form=form)


# Set the login view for the login route
login.login_view = 'connexion'


@app.route("/user/logout", methods=["POST", "GET"])
def logout():
    if current_user.is_authenticated is True:
        logout_user()
    flash("You have been loged out", "info")
    return redirect(url_for("home"))