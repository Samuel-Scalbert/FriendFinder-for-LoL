from flask import url_for, render_template, redirect, request, flash
from ..models.data_base import Users
from ..models.formulaires import ChooseAccount, AccountFollowed
from ..utils.transformations import clean_arg
import requests
from ..app import app
from flask_login import login_user, current_user,  logout_user, login_required
from  ..API_lol.match_records import match_records

@app.route("/match/chooseaccount", methods=['GET', 'POST', 'HEAD'])
def select_account():
    form = ChooseAccount(current_user.id)
    form.account.choices = [(account.id, account.username) for account in AccountFollowed.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        selected_account_id = form.account.data
        selected_account = AccountFollowed.query.get(selected_account_id)
        selected_username = selected_account.username
        return redirect(url_for('get_match', username=selected_username))
    return render_template('pages/select_account.html', form=form)
@app.route('/match/match_records/<username>', methods=["GET", "POST"])
# Goal: catching important rates for a given match: KDA, Creep score, Magic blows' success and damages, and Gold entries.
@login_required
def get_match(username):
    data = match_records(username)
    print(data)
    return render_template("pages/match_records.html", data=data)

