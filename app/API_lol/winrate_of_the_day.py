import datetime
import requests
from ..app import api_key
import time
from flask import flash

def winrate(summoner):
## set the time of today
    now = datetime.datetime.now()

    start_of_day = datetime.datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=0,
        minute=0,
        second= 1,
    )

    end_of_day = datetime.datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=23,
        minute=59,
        second=59,
    )

    ## retrieve the start of the day and the end of the day

    end_of_day_epoch = str(int(end_of_day.timestamp()))
    start_of_day_epoch = str(int(start_of_day.timestamp()))

    w = 0
    l = 0
    wr = 0
    winrate = []
    data_summoner = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner + '?api_key=' + api_key).json()
    if "id" in data_summoner:
        puuid_summoner = data_summoner.get("puuid")

        ## with the id, the end of the day, and the start of the day we can check if the account has done any SOLOQ for the day

        matches_id = requests.get(
            'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid_summoner + '/ids?queue=' + '420' + '&startTime=' + start_of_day_epoch + '&endTime=' + end_of_day_epoch + '&count=20&api_key=' + api_key).json()

        ## check if there is any match
        if len(matches_id) != 0:
            for match_id in matches_id:
            ## check the result of the game for the summoner
                try:
                    match_info = requests.get("https://europe.api.riotgames.com/lol/match/v5/matches/" + match_id + "?api_key=" + api_key).json()
                    for player in (match_info['info']['participants']):
                        if player['puuid'] == puuid_summoner:
                            if player['win'] == True:
                                w += 1
                            else:
                                l += 1
                except KeyError:
                    time.sleep(2)
            try:
                wr = (w / (w + l)) * 100
            except ZeroDivisionError:
                flashs = True
                winrate.append(None)
                winrate.append(summoner)
                return winrate, flashs
            winrate.append("{:.1f}".format(wr))
            winrate.append(w + l)
            winrate.append(summoner)
        elif len(matches_id) == 0:
            winrate.append(None)
            winrate.append(summoner)
    return winrate
