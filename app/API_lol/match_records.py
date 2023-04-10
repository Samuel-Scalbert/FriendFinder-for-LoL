import requests
from ..app import api_key
from flask import url_for, render_template, redirect, request, flash
import json

def match_records(username):

    data_summoner = requests.get(
        'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + username + '?api_key=' + api_key).json()
    if data_summoner is not None and "id" in data_summoner:
        puuid_summoner = data_summoner.get("puuid")

        matchs_id = requests.get(
            f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid_summoner}/ids?queue=420&type=ranked&start=0&count=1&api_key={api_key}").json()
        for match_id in matchs_id:
            match = requests.get(
                "https://europe.api.riotgames.com/lol/match/v5/matches/" + match_id + "?api_key=" + api_key)
            with match as f:
                print(match)
                ce_match = f.json()

                id = ce_match["metadata"]["matchId"]

                for elt in ce_match["info"]["participants"]:

                    match_records = []

                    champion = elt["championName"]
                    kda = (elt["challenges"]["kda"])
                    gains = elt["goldEarned"]
                    expenses = elt["goldSpent"]
                    golds = gains - expenses
                    creep_score = elt["neutralMinionsKilled"]
 
                    dealt = elt["magicDamageDealt"]
                    taken = elt["magicDamageTaken"]
                    magic_damage_update = dealt - taken

                    # Final records
                    match_records.append(id)
                    match_records.append(champion)
                    match_records.append(kda)
                    match_records.append(golds)
                    match_records.append(creep_score)
                    match_records.append(magic_damage_update)

                    data = match_records
        return data
