
import requests

api_key = "RGAPI-43e6bcf8-2b3c-46b1-b5fe-3ae242586236"

## récupère puis stocke le PUUID du summoner

#summonerName = input("Summoner Name:")

data_summoner = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/SaintLoutr?api_key=RGAPI-43e6bcf8-2b3c-46b1-b5fe-3ae242586236'+ 'SaintLoutr' +'?api_key='+api_key).json()
puuid_summoner = data_summoner.get("puuid")
print("puuid =", puuid_summoner)

#LEADERBOARD : 
# Je veux récupérer le championLevel, un classement des champions par niveau : sort, valeur moyenne

#Je récupère l'ID des champions : itérer sur la liste, puis sur le dictionnaire

champion_id = requests.get('https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/kgDgl2ZnQEIRdaLH_wdzI_oSNC-Df0fZ7bnQDiqiB0sTdlxEoVmCuTZPjg/top?api_key=RGAPI-43e6bcf8-2b3c-46b1-b5fe-3ae242586236'+ champion_id +"?api_key=" + api_key).json()

resultats = [
    {"championId": 161, "championLevel": 7, "championPoints": 62207},
    {"championId": 81, "championLevel": 6, "championPoints": 53193},
    {"championId": 145, "championLevel": 6, "championPoints": 51950}
]

# parcourir les dictionnaires de chaque champion
for champion in resultats:
    # récupérer l'ID du champion
    champion_id = champion["championId"]
    print(champion_id)

