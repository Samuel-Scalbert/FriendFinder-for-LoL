from flask import url_for, render_template, redirect, request, flash
from ..models.data_base import  AccountFollowed, DataRanking
from ..models.formulaires import NewFollower
from ..utils.transformations import clean_arg
from ..app import app
from sqlalchemy import case
import roman
from  ..API_lol.API_check import API_check
from  ..API_lol.winrate_of_the_day import winrate
from  ..API_lol.data_account import summmoner_opgg

# Define a route for adding an account as a friend
@app.route('/my_friends/add_account', methods=['GET', 'POST'])
@login_required
def add_account():
    # Check if the API is available
    if API_check() == True:
        # Create a new form for adding a follower
        form = NewFollower()
        # If the form is submitted and valid
        if form.validate_on_submit():
            # Add the account to the list of friends
            statut, donnees = AccountFollowed.ajout_account(username=clean_arg(request.form.get("username")))
            # If the account is added successfully
            if statut is True:
                # Display a success message and redirect to the add account page
                flash("This account has been added to your friend list !", "success")
                return redirect(url_for("add_account"))
            # If the account cannot be added
            else:
                # Display an error message and return to the add follower form
                flash(",".join(donnees), "info")
                return render_template("pages/new_follower.html", form=form)
        # If the form is not submitted or not valid
        else:
            # Return the add follower form
            return render_template("pages/new_follower.html", form=form)
    # If the API is not available
    else:
        # Display a message and return to the home page
        flash('The API might be over flooded right now wait a minute please', "info")
        return render_template("pages/home.html")

# Define a route for displaying a list of friends
@app.route('/my_friends/list_of_friends', methods=['GET'])
@login_required
def list_of_friends():
    # Query the database for the list of friends and their ranks
    list_rank = DataRanking.query.with_entities(DataRanking.summoner_name, DataRanking.rank, DataRanking.tier,DataRanking.lp, DataRanking.lp_diff).filter_by(
        account_followed_id=current_user.id).order_by(
        case(
            (DataRanking.rank == 'CHALLENGER', 1),
            (DataRanking.rank == 'GRANDMASTER', 2),
            (DataRanking.rank == 'MASTER', 3),
            (DataRanking.rank == 'DIAMOND', 4),
            (DataRanking.rank == 'PLATINUM', 5),
            (DataRanking.rank == 'GOLD', 6),
            (DataRanking.rank == 'SILVER', 7),
            (DataRanking.rank == 'BRONZE', 8),
            (DataRanking.rank == 'IRON', 9),
            else_=10
        ).asc(),
        DataRanking.tier.asc(),
        DataRanking.lp.desc()).all()
    # Convert the rank numbers to Roman numerals and add the op.gg link for each friend
    for i in range(len(list_rank)):
        number = list_rank[i][2]
        number_roman = roman.toRoman(number)
        list_rank[i] = (list_rank[i][0], list_rank[i][1], number_roman, list_rank[i][3],list_rank[i][4], summmoner_opgg(list_rank[i][0]))
    # Return the list of friends template with the friend data
    return render_template("pages/my_friends.html", list_rank=list_rank)


# This is a Flask route decorator that binds a URL path to a function that handles the request
@app.route('/my_friends/my_friends/update', methods=['GET'])
# A function called 'update_friends' that returns a response object to the client
def update_friends():
    # A conditional statement that checks the value returned by a function called 'API_check' and performs an action depending on the result
    if API_check() == True:

        # A new empty list named 'list_username'
        list_username = []

        # A database query that retrieves a column 'summoner_name' from a table called 'DataRanking' where 'account_followed_id' matches the current user's ID
        list_update_row = DataRanking.query.with_entities(DataRanking.summoner_name).filter_by(
            account_followed_id=current_user.id).all()

        # A for loop that iterates over the query result and appends each value to the 'list_username' list after converting it to a string
        for name in list_update_row:
            list_username.append(((",".join(name))))

        # A for loop that iterates over each string in the 'list_username' list and updates the account of each user using a function called 'update_account'
        # The function returns the updated league points
        for name in list_username:
            league_points = AccountFollowed.update_account(name)

        # Redirects to a function called 'list_of_friends'
        return redirect(url_for("list_of_friends"))

    # An else statement that executes if the value returned by 'API_check' is not True
    else:
        # A flash message that displays an informational message to the user
        flash('The API might be over flooded right now wait a minute please', "info")

        # Renders a template called 'home.html'
        return render_template("pages/home.html")

# This is a route decorator which binds the URL path '/my_friends/winrate' with this function.
@app.route('/my_friends/winrate', methods=['GET'])

# The 'login_required' decorator is used to prevent unauthenticated users from accessing this function.
@login_required

# This function is defined with the name 'winrate_friends'.
def winrate_friends():

    # Set the value of the 'flashs' variable to False.
    flashs = False

    # Create an empty list called 'list_username'.
    list_username = []

    # Create an empty list called 'account_updated'.
    account_updated = []

    # Query the 'DataRanking' table for all rows where the 'account_followed_id' column matches the current user's id.
    # Get only the 'summoner_name' column from these rows.
    # Store the resulting rows in 'list_update_row'.
    list_update_row = DataRanking.query.with_entities(DataRanking.summoner_name).filter_by(account_followed_id=current_user.id).all()

    # For each name in 'list_update_row', join the strings with a comma and append it to 'list_username'.
    for name in list_update_row:
        list_username.append((",".join(name)))

    # For each name in 'list_username', check if the API is available.
    # If the API is not available, flash a message and break the loop.
    # Otherwise, get the winrate for the name using the 'winrate' function and append it to 'account_updated'.
    for name in list_username:
        if not API_check():
            flash('The API might be over flooded right now wait a minute please', "info")
            break
        winrates = winrate(name)
        if flashs == True:
            flash('The API might be over flooded right now wait a minute please', "info")
            return render_template("pages/winrate.html", account_updated=account_updated)
        else:
            account_updated.append(winrates)

    # Render the 'winrate.html' template, passing in the 'account_updated' list as a parameter.
    return render_template("pages/winrate.html", account_updated=account_updated)


