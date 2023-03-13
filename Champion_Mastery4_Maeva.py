import requests

api_key = "RGAPI-da61b6ab-9c45-44a3-8e34-9139fc111b7c"

## récupère puis stocke l'ID du summoner
summoner_name = input("Summoner Name : ")
champions_count = int(input("Nombre de champions à afficher : "))

# On vérifie le nombre saisi par l'utilisateur parce qu'il ne faut jamais faire confiance à l'utilisateur
if champions_count < 1:
    print("Nombre de champions à afficher invalide")
    exit()


data_summoner = requests.get(
    f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
).json()


# print("data-summoner =", data_summoner)
summoner_id = data_summoner.get("id")
print("summoner_id =", summoner_id)


#LEADERBOARD : 
# Je veux récupérer le championLevel, un classement des champions par :
# - niveau (par points, plus précis que par niveau)
# - sort
# - valeur moyenne
# Je récupère l'ID des champions : itérer sur la liste, puis sur le dictionnaire


# On récupère les meilleurs champions du joueur, limités au nombre de champions_count
# champions = requests.get(
#     f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}/top?api_key={api_key}&count={champions_count}"
# ).json()

# # On récupère tous les champions du joueur
champions = requests.get(
    f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}?api_key={api_key}"
).json()


# On affiche la réponse de la requête précédente
# print("champions =", champions)


# Je récupère seulement les informations qui m'intéressent sur les champions et je limite le nombre de champions à afficher
champions_data = []
for champion in champions[:int(champions_count)]:
    champions_data.append( {
        "id": champion["championId"],
        "points": champion["championPoints"],
        "tokens": champion["tokensEarned"],
    } )



# On trie les champions par ordre décroissant de points
# La copie est faite car sort modifie la liste et on ne veut pas modifier la liste originale
champions_sorted_by_points = champions_data.copy()
champions_sorted_by_points.sort(key=lambda champion : champion["points"], reverse=True)

# On trie les champions par ordre décroissant de tokens
# La copie est faite car sort modifie la liste et on ne veut pas modifier la liste originale
champions_sorted_by_tokens = champions_data.copy()
champions_sorted_by_tokens.sort(key=lambda champion : champion["tokens"], reverse=True)



print("\nListe des Champions originale")
for i, d in enumerate(champions_sorted_by_points):
    print(f"{i+1}. Champion {d['id']}: {d['points']} points ; {d['tokens']} tokens")


print("\nListe des Champions triée par points")
for i, d in enumerate(champions_sorted_by_points):
    print(f"{i+1}. Champion {d['id']}: {d['points']} points")


print("\nListe des Champions triée par tokens")
for i, d in enumerate(champions_sorted_by_tokens):
    print(f"{i+1}. Champion {d['id']}: {d['tokens']} tokens")