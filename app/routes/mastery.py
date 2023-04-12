from flask import url_for, render_template, redirect, request, flash
from ..models.data_base import Users
from ..models.formulaires import ChooseAccount, AccountFollowed
from ..utils.transformations import clean_arg
import requests
from ..app import app
from flask_login import login_user, current_user,  logout_user, login_required
from  ..API_lol.mastery import mastery_recap

@app.route("/mastery/chooseaccount", methods=['GET', 'POST', 'HEAD'])
@login_required
def select_account_mastery():
    form = ChooseAccount(current_user.id)
    form.account.choices = [(account.id, account.username) for account in AccountFollowed.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        selected_account_id = form.account.data
        selected_account = AccountFollowed.query.get(selected_account_id)
        selected_username = selected_account.username
        return redirect(url_for('get_mastery', username=selected_username))
    return render_template('pages/select_account_mastery.html', form=form)
@app.route('/mastery/mastery_records/<username>', methods=["GET", "POST"])
@login_required
def get_mastery(username):
    data = mastery_recap(username,5)
    data_all_champions = []
    for data in data:
        data_one_champion = [username,data['name'],data['points'], ("http://ddragon.leagueoflegends.com/cdn/img/champion/loading/"+ data['name'] +"_0.jpg")]
        data_all_champions.append(data_one_champion)
    print(data_all_champions)
    return render_template("pages/mastery.html", data=data_all_champions)

