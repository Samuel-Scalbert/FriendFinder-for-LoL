# import the datetime, requests, and flash modules
import datetime
import requests
from ..app import api_key
import time
from flask import flash

# define a function named 'winrate' that takes a summoner as input
def winrate(summoner):

    # set the current date and time
    now = datetime.datetime.now()

    # set the start of the day to the current year, month, and day at 12:00:01am
    start_of_day = datetime.datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=0,
        minute=0,
        second= 1,
    )

    # set the end of the day to the current year, month, and day at 11:59:59pm
    end_of_day = datetime.datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=23,
        minute=59,
        second=59,
    )

    # get the epoch time of the start and end of the day
    end_of_day_epoch = str(int(end_of_day.timestamp()))
    start_of_day_epoch = str(int(start_of_day.timestamp()))

    # initialize variables to keep track of wins, losses, and winrate
    w = 0
    l = 0
    wr = 0
    winrate = []

    # use the Riot Games API to get information about the summoner
    data_summoner = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner + '?api_key=' + api_key).json()

    # check if the summoner exists
    if "id" in data_summoner:

        # get the summoner's unique identifier
        puuid_summoner = data_summoner.get("puuid")

        # use the Riot Games API to get the list of matches played by the summoner on this day
        matches_id = requests.get(
            'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid_summoner + '/ids?queue=' + '420' + '&startTime=' + start_of_day_epoch + '&endTime=' + end_of_day_epoch + '&count=20&api_key=' + api_key).json()

        # check if there are any matches played by the summoner
        # Check if there are any matches for the given summoner
        if len(matches_id) != 0:
            # Loop through each match and check if the summoner won or lost
            for match_id in matches_id:
                try:
                    # Use the Riot Games API to get information about the match
                    match_info = requests.get(
                        "https://europe.api.riotgames.com/lol/match/v5/matches/" + match_id + "?api_key=" + api_key).json()
                    # Loop through each player in the match and check if the player is the summoner
                    for player in (match_info['info']['participants']):
                        if player['puuid'] == puuid_summoner:
                            # Increment the win counter if the summoner won, and the loss counter otherwise
                            if player['win'] == True:
                                w += 1
                            else:
                                l += 1
                except KeyError:
                    # Wait for 2 seconds before retrying in case of a KeyError
                    time.sleep(2)
            try:
                # Calculate the summoner's winrate
                wr = (w / (w + l)) * 100
            except ZeroDivisionError:
                # Set flashs to True, append None to winrate list, and return the winrate list with summoner name
                flashs = True
                winrate.append(None)
                winrate.append(summoner)
                return winrate, flashs
            # Append the winrate, number of games played, and summoner name to the winrate list
            winrate.append("{:.1f}".format(wr))
            winrate.append(w + l)
            winrate.append(summoner)
        # If there are no matches for the summoner, append None and the summoner name to the winrate list
        elif len(matches_id) == 0:
            winrate.append(None)
            winrate.append(summoner)
        # Return the winrate list
        return winrate

