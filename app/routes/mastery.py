from flask import url_for, render_template, redirect, request, flash
from ..models.data_base import Users
from ..models.formulaires import ChooseAccount, AccountFollowed
from ..utils.transformations import clean_arg
import requests
from ..app import app
from flask_login import login_user, current_user,  logout_user, login_required
from  ..API_lol.mastery import mastery_recap


# This route decorator sets the route to "/mastery/chooseaccount" and specifies the allowed methods
@app.route("/mastery/chooseaccount", methods=['GET', 'POST', 'HEAD'])
# This decorator ensures that the user is logged in before executing the function
@login_required
# This function handles the select_account_mastery route
def select_account_mastery():
    # Creates an instance of the ChooseAccount form
    form = ChooseAccount(current_user.id)

    # Sets the choices for the account dropdown menu
    # The choices are the username and id for each account followed by the current user
    # The list is created using a list comprehension
    # The list comprehension queries the AccountFollowed table and filters by the current_user's id
    form.account.choices = [(account.id, account.username) for account in
                            AccountFollowed.query.filter_by(user_id=current_user.id).all()]

    # If the form is submitted and valid
    if form.validate_on_submit():
        # Gets the selected account's id from the form
        selected_account_id = form.account.data

        # Queries the AccountFollowed table for the selected account
        selected_account = AccountFollowed.query.get(selected_account_id)

        # Gets the selected account's username
        selected_username = selected_account.username

        # Redirects the user to the get_mastery route with the selected_username as a parameter
        return redirect(url_for('get_mastery', username=selected_username))

    # Renders the select_account_mastery.html template with the ChooseAccount form
    return render_template('pages/select_account_mastery.html', form=form)


# This route decorator sets the route to "/mastery/mastery_records/<username>" and specifies the allowed methods
@app.route('/mastery/mastery_records/<username>', methods=["GET", "POST"])
# This decorator ensures that the user is logged in before executing the function
@login_required
# This function handles the get_mastery route with a parameter of username
def get_mastery(username):
    # Calls the mastery_recap function and sets the returned data to the data variable
    data = mastery_recap(username, 5)

    # Creates an empty list for all the champion data
    data_all_champions = []

    # Iterates through each champion's data
    for data in data:
        # Creates a list with the username, champion name, champion mastery points, and image URL for the champion
        data_one_champion = [username, data['name'], data['points'],
                             ("http://ddragon.leagueoflegends.com/cdn/img/champion/loading/" + data['name'] + "_0.jpg")]

        # Adds the champion data to the data_all_champions list
        data_all_champions.append(data_one_champion)

    # Prints the data_all_champions list to the console
    print(data_all_champions)

    # Renders the mastery.html template with the data_all_champions list
    return render_template("pages/mastery.html", data=data_all_champions)

