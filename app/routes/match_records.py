from flask import url_for, render_template, redirect, request, flash
from ..models.data_base import Users
from ..models.formulaires import ChooseAccount, AccountFollowed
from ..utils.transformations import clean_arg
import requests
from ..app import app
from flask_login import login_user, current_user,  logout_user, login_required
from  ..API_lol.match_records import match_records

# Importing Flask module
from flask import Flask, render_template, request, redirect, url_for, flash
# Importing current_user, login_required, and other relevant modules
from flask_login import current_user, login_required
# Importing ChooseAccount, AccountFollowed, and match_records classes from other modules
from .forms import ChooseAccount
from .models import AccountFollowed, match_records

# Defining a route for selecting an account
@app.route("/match/chooseaccount", methods=['GET', 'POST', 'HEAD'])
# Login is required to access this route
@login_required
def select_account():
    # Creating an instance of the ChooseAccount class
    form = ChooseAccount(current_user.id)
    # Populating the account selection dropdown with accounts followed by the user
    form.account.choices = [(account.id, account.username) for account in AccountFollowed.query.filter_by(user_id=current_user.id).all()]
    # If the form is submitted and validated
    if form.validate_on_submit():
        # Get the selected account ID and the corresponding account instance
        selected_account_id = form.account.data
        selected_account = AccountFollowed.query.get(selected_account_id)
        # Get the username of the selected account
        selected_username = selected_account.username
        # Redirect the user to the match records page for the selected account
        return redirect(url_for('get_match', username=selected_username))
    # If the form is not submitted or validated, render the select account page with the ChooseAccount form
    return render_template('pages/select_account_match.html', form=form)

# Defining a route for getting match records
@app.route('/match/match_records/<username>', methods=["GET", "POST"])
# Login is required to access this route
@login_required
def get_match(username):
    # Get the match records for the given username
    data = match_records(username)
    # Print the match records to the console (for debugging purposes)
    print(data)
    # Render the match records page with the match data and the username
    return render_template("pages/match_records.html", data=data, username=username)


