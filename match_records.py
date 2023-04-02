from flask import url_for, render_template, redirect, request, flash
import requests
from ..models.data_base import  AccountFollowed, DataRanking
from ..models.formulaires import MatchFinder
from ..utils.transformations import clean_arg
from ..app import app
from flask_login import  current_user, login_required
from sqlalchemy import case
import roman
import json

@app.route("/")
@app.route('match_records', methods=["GET","POST"])
#Goal: catching important rates for a given match: KDA, Creep score, Magic blows' success and damages, and Gold entries.
@login_required
def get_match():
     for request in range(5):
        total_records = []   
        form = MatchFinder()
        if form.validate_on_submit(): statut, donnees = clean_arg(request.form.get("puuid"))
        
        try:
                match = requests.get(f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{donnees}/ids?queue=420&type=ranked&start=0&count=1&api_key={api_key}").json()
                
        except FileNotFoundError:
                flash("Did you copy the right PUUID?", "info") #Ou deviez-vous inscrire "puuid" à la place de "donnees"?
                return render_template("pages/match_finder.html", form=form)
                
        except SyntaxError:
                flash("Votre dev ne sait pas écrire une requête en .get. Invoquez Saint Samuel Scalbert.")
                return render_template("pages/match_finder.html", form=form)
                        
        if statut is True:
                match = requests.get(f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{donnees}/ids?queue=420&type=ranked&start=0&count=1&api_key={api_key}").json()

                with open("match.json()") as f:
                        ce_match = json.load(f)

                        id = ce_match["metadata"]["matchId"]
                                
                        for elt in ce_match["info"]["participants"]:

                                match_records = [] 

                                champion = elt["championName"]
                                kda = (elt["challenges"]["kda"])
                                gains = elt["goldEarned"]
                                expenses = elt["goldSpent"]
                                golds = gains - expenses
                                creep_score = elt["neutralMinionsKilled"]
                                if creep_score < 100:
                                        flash("That doesn't make you a lesser threat.")
                                if creep_score > 100 < 200:
                                        flash("Keep going strong!")
                                if creep_score > 200:
                                        flash("And what's next?")    
                                dealt = elt["magicDamageDealt"]
                                taken = elt["magicDamageTaken"]
                                magic_damage_update = dealt - taken
                                if magic_damage_update > 0:
                                        flash("You're a killer, baby!")
                                else:
                                        flash("Just pull yourself together.")
                                #messages conditionnels à virer s'ils posent problème au HTML, ce qui ne manquera pas d'arriver vue la non subtilité avec laquelle le template fut pensé           
                                
                                        #Final records
                                match_records.append(id)        
                                match_records.append(champion)
                                match_records.append(kda)
                                match_records.append(golds)
                                match_records.append(creep_score)
                                match_records.append(magic_damage_update)

                                data = match_records

                        return render_template("pages/match_records.html/body/div[class='match']", data=data)





                                


                                
