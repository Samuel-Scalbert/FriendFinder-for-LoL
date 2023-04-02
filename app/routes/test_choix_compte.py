from ..app import app, login
from flask import url_for, render_template, redirect, flash
from ..models.formulaires import ChooseAccount
from ..models.data_base import AccountFollowed
from flask_login import current_user

@app.route("/test/chooseaccount", methods=['GET', 'POST', 'HEAD'])
def select_account():
    form = ChooseAccount(current_user.id)ghfty
    form.account.choices = [(account.id, account.username) for account in AccountFollowed.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        selected_account_id = form.account.data
        selected_account = AccountFollowed.query.get(selected_account_id)
        selected_username = selected_account.username
        return redirect(url_for('account_page', username=selected_username))
    return render_template('pages/select_account.html', form=form)

@app.route('/test/chooseaccount/<username>', methods=['GET', 'POST','HEAD'])
def account_page(username):
    print(f"Page du compte pour l'utilisateur {username}")
    return render_template("pages/home.html")