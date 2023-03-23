import requests
from ..app import api_key
import roman

def ranking_information(summoner):
    list_summoner_rank = []
        ## retrieve the id of the account
    data_summoner = requests.get(
        'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner + '?api_key=' + api_key).json()
    if data_summoner is not None and "id" in data_summoner:
        id_summoner = data_summoner.get("id")

        ## with the id we can retrieve the information of the account (tier, LP, rank)

        data_rank = requests.get(
            'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + id_summoner + '?api_key=' + api_key).json()

        ## we check from the data_rank if the account has done any SOLO Q games for this season only !!

        presence_of_soloq_data = False
        for data_SOLOQ in data_rank:
            if data_SOLOQ['queueType'] == "RANKED_SOLO_5x5":
                rank = data_SOLOQ['rank']
                rank_roman = roman.fromRoman(rank)
                ## here we save the informations for each account

                list_summoner_rank = [summoner, data_SOLOQ['tier'], rank_roman, data_SOLOQ['leaguePoints']]
                presence_of_soloq_data = True
        if not presence_of_soloq_data:
            ## we still keep the summoner (to avoid users thinking that the account was not checked)
            list_summoner_rank = None
    else:
        list_summoner_rank = []
    return list_summoner_rank