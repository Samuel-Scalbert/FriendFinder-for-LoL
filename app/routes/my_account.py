from flask import url_for, render_template, redirect, request, flash
from ..models.data_base import  AccountFollowed, DataRanking
from ..models.formulaires import NewFollower
from ..utils.transformations import clean_arg
from ..app import app
from flask_login import  current_user, login_required
from sqlalchemy import case
import roman
from  ..API_lol.winrate_of_the_day import winrate
from  ..API_lol.API_check import API_check

@app.route('/my_account/add_account', methods=['GET', 'POST'])
@login_required
def add_account():
    if API_check() == True:
        form = NewFollower()
        if form.validate_on_submit():
            statut, donnees = AccountFollowed.ajout_account(username=clean_arg(request.form.get("username")))
            if statut is True:
                flash("This account has been added to your friend list !", "success")
                return redirect(url_for("add_account"))
            else:
                flash(",".join(donnees), "info")
                return render_template("pages/new_follower.html", form=form)
        else:
            return render_template("pages/new_follower.html", form=form)
    else:
        flash('The API might be over flooded right now wait a minute please', "info")
        return render_template("pages/home.html")

@app.route('/my_account/my_friends', methods=['GET'])
@login_required
def my_friends():
    list_rank = DataRanking.query.with_entities(DataRanking.summoner_name, DataRanking.rank,DataRanking.tier,DataRanking.lp).filter_by(
        account_followed_id=current_user.id).order_by(
        case([(DataRanking.rank == 'CHALLENGER', 1),
              (DataRanking.rank == 'GRANDMASTER', 2),
              (DataRanking.rank == 'MASTER', 3),
              (DataRanking.rank == 'DIAMOND', 4),
              (DataRanking.rank == 'PLATINUM', 5),
              (DataRanking.rank == 'GOLD', 6),
              (DataRanking.rank == 'SILVER', 7),
              (DataRanking.rank == 'BRONZE', 8),
              (DataRanking.rank == 'IRON', 9)],
             else_=10).asc(),
        DataRanking.tier.asc(),
        DataRanking.lp.desc()).all()
    for i in range(len(list_rank)):
        number = list_rank[i][2]
        number_roman = roman.toRoman(number)
        list_rank[i] = (list_rank[i][0], list_rank[i][1], number_roman, list_rank[i][3])
    return render_template("pages/my_friends.html", list_rank=list_rank)

@app.route('/my_account/my_friends/update', methods=['GET'])
def update_friends():
    if API_check() == True:
        list_username = []
        list_update_row = DataRanking.query.with_entities(DataRanking.summoner_name).filter_by(account_followed_id=current_user.id).all()
        for name in list_update_row:
            list_username.append(((",".join(name))))
        for name in list_username:
            AccountFollowed.update_account(name)
        return redirect(url_for("my_friends"))
    else:
        flash('The API might be over flooded right now wait a minute please', "info")
        return render_template("pages/home.html")

@app.route('/my_account/winrate', methods=['GET'])
@login_required
def winrate_friends():
    flashs = False
    list_username = []
    account_updated = []
    list_update_row = DataRanking.query.with_entities(DataRanking.summoner_name).filter_by(account_followed_id=current_user.id).all()
    for name in list_update_row:
        list_username.append((",".join(name)))
    for name in list_username:
        if not API_check():
            flash('The API might be over flooded right now wait a minute please', "info")
            break
        winrates = winrate(name)
        print(winrates)
        print(flash)
        if flashs == True:
            flash('The API might be over flooded right now wait a minute please', "info")
            return render_template("pages/winrate.html", account_updated=account_updated)
        else:
            account_updated.append(winrates)
    return render_template("pages/winrate.html", account_updated=account_updated)

