from ..app import app, db, api_key
from flask import url_for, render_template, redirect, request, flash
from sqlalchemy import or_
from ..models.data_base import Users
from  ..API_lol.data_account import ranking_information


@app.route("/")
@app.route("/home")
def home():
    return render_template("pages/home.html")

@app.route("/")
@app.route("/data_rank")
def data_rank():
    data = ranking_information(["SaintLoutr"])
    print(data)
    return render_template("pages/data.html",data = data)