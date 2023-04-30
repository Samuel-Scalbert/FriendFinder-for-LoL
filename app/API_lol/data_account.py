import requests  # importing requests module to send HTTP requests
from ..app import api_key  # importing api_key from the app module
import roman  # importing roman module to convert roman numerals
from urllib.parse import quote  # importing quote function from the urllib.parse module

def ranking_information(summoner):
    list_summoner_rank = []  # creating an empty list to store information of summoner's ranking

    # sending an HTTP GET request to Riot Games API to get information about the summoner
    data_summoner = requests.get(
        'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner + '?api_key=' + api_key).json()

    # checking if data_summoner contains any information and if it contains the "id" key
    if data_summoner is not None and "id" in data_summoner:
        id_summoner = data_summoner.get("id")  # retrieving the summoner's ID from data_summoner

        # sending an HTTP GET request to Riot Games API to get the summoner's ranking information
        data_rank = requests.get(
            'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + id_summoner + '?api_key=' + api_key).json()

        presence_of_soloq_data = False  # setting presence_of_soloq_data variable to False initially
        # iterating over each element of data_rank and checking if it is for "RANKED_SOLO_5x5" queue type
        for data_SOLOQ in data_rank:
            if data_SOLOQ['queueType'] == "RANKED_SOLO_5x5":
                rank = data_SOLOQ['rank']  # retrieving the summoner's rank from data_SOLOQ
                rank_roman = roman.fromRoman(rank)  # converting the rank to roman numeral format

                # storing the summoner's ranking information in list_summoner_rank
                list_summoner_rank = [summoner, data_SOLOQ['tier'], rank_roman, data_SOLOQ['leaguePoints']]
                presence_of_soloq_data = True  # setting presence_of_soloq_data to True if data_SOLOQ is for "RANKED_SOLO_5x5"

        # checking if presence_of_soloq_data is still False, which means no SOLO Q game was played by the summoner
        if not presence_of_soloq_data:
            list_summoner_rank = None  # setting list_summoner_rank to None to indicate no SOLO Q games played

    else:
        list_summoner_rank = []  # setting list_summoner_rank to empty list if data_summoner doesn't contain the "id" key

    return list_summoner_rank  # returning the summoner's ranking information as a list


def summmoner_opgg(summoner):
    player_name = summoner  # storing the summoner name in player_name variable
    encoded_player_name = quote(player_name)  # encoding the summoner name using the quote function
    opgg_url = f"https://www.op.gg/summoners/euw/{encoded_player_name}"  # creating the op.gg URL for the summoner
    return opgg_url  # returning the op.gg URL for the summoner
