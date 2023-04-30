# Import necessary modules
import requests  # Module for making HTTP requests
from ..app import api_key  # Import api_key from parent directory's app module
from flask import url_for, render_template, redirect, request, flash  # Web framework
import json  # For working with JSON data

# Define function to retrieve match records for a given username
def match_records(username):

    # Make request to Riot Games API to get summoner data for the given username
    data_summoner = requests.get(
        'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + username + '?api_key=' + api_key).json()

    # Check if summoner data exists and has an ID
    if data_summoner is not None and "id" in data_summoner:

        # Get the summoner's unique identifier
        puuid_summoner = data_summoner.get("puuid")

        # Initialize list to store match records
        match_records= []

        # Get a list of match IDs for the summoner's recent ranked games
        matchs_id = requests.get(
            f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid_summoner}/ids?queue=420&type=ranked&start=0&count=5&api_key={api_key}").json()

        # Loop through each match ID and retrieve the match data
        for match_id in matchs_id:
            match = requests.get(
                "https://europe.api.riotgames.com/lol/match/v5/matches/" + match_id + "?api_key=" + api_key)

            # Retrieve the JSON response from the API call
            with match as f:
                this_match = f.json()

                # Get the match ID
                id = this_match["metadata"]["matchId"]

                # Loop through each participant in the match
                for elt in this_match["info"]["participants"]:
                    this_match_records = []

                    # Check if the participant is the same as the summoner we're interested in
                    if elt["puuid"] == puuid_summoner:

                        # Extract relevant information about the participant's performance
                        champion = elt["championName"]
                        champion_ID = elt["championId"]
                        kda_float = (elt["challenges"]["kda"])
                        kda = "{:.2f}".format(kda_float)
                        golds = elt["goldEarned"]
                        creep_score = elt["totalMinionsKilled"]
                        damage = elt["totalDamageDealtToChampions"]
                        result = elt["win"]

                        # Append the extracted information to the match record list
                        this_match_records.append(id)
                        this_match_records.append(champion)
                        this_match_records.append(kda)
                        this_match_records.append(golds)
                        this_match_records.append(creep_score)
                        this_match_records.append(damage)
                        this_match_records.append(champion_ID)
                        this_match_records.append(result)

                        # Append the match record to the list of match records
                        match_records.append(this_match_records)

                    # Set data to match_records list
                    data = match_records

        # Return the list of match records
        return data
