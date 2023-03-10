
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


# Pour afficher  le classement des joueurs, triés par ordre décroissant des points de champion :

data = [
    {
        "championId": 161,
        "championLevel": 7,
        "championPoints": 62207,
        "lastPlayTime": 1677889540000,
        "championPointsSinceLastLevel": 40607,
        "championPointsUntilNextLevel": 0,
        "chestGranted": true,
        "tokensEarned": 0,
        "summonerId": "kgDgl2ZnQEIRdaLH_wdzI_oSNC-Df0fZ7bnQDiqiB0sTdlxEoVmCuTZPjg"
    },
    {
        "championId": 81,
        "championLevel": 6,
        "championPoints": 53193,
        "lastPlayTime": 1678039068000,
        "championPointsSinceLastLevel": 31593,
        "championPointsUntilNextLevel": 0,
        "chestGranted": true,
        "tokensEarned": 3,
        "summonerId": "kgDgl2ZnQEIRdaLH_wdzI_oSNC-Df0fZ7bnQDiqiB0sTdlxEoVmCuTZPjg"
    },
    {
        "championId": 145,
        "championLevel": 6,
        "championPoints": 51950,
        "lastPlayTime": 1676480533000,
        "championPointsSinceLastLevel": 30350,
        "championPointsUntilNextLevel": 0,
        "chestGranted": false,
        "tokensEarned": 2,
        "summonerId": "kgDgl2ZnQEIRdaLH_wdzI_oSNC-Df0fZ7bnQDiqiB0sTdlxEoVmCuTZPjg"
    }
]

sorted_data = sorted(data, key=lambda x: x['championPoints'], reverse=True)

for i, d in enumerate(sorted_data):
    print(f"{i+1}. Champion {d['championId']}: {d['championPoints']} points")
