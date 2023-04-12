import requests
#from ..app import api_key

api_key = "RGAPI-ccedf9be-d967-4fba-b200-a09887cb94af"

# Récupère les versions du jeu
version_patch = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()
# Récupère la dernière version du jeu
version_patch = version_patch[0]
# Récupère les données des champions en francais a partir de la derniere version du jeu
# Stocke les données des champions dans la variable data_full_champion
data_full_champion = requests.get(
    'https://ddragon.leagueoflegends.com/cdn/' + version_patch + '/data/fr_FR/champion.json').json()
# Stocke les données des champions dans la variable data_champion_by_name
data_champion_by_name = data_full_champion["data"]


# Definition de la fonction get_champion_name_by_id qui récupère le nom d'un champion à partir de son ID
def get_champion_name_by_id(id):
    # utilisation de la variable globale data_champion_by_name
    global data_champion_by_name
    # On parcourt la liste des champions
    for name in data_champion_by_name:
        # On vérifie si l'id du champion correspond à l'id du champion recherché
        if data_champion_by_name[name]['key'] == str(id):
            # Si oui, on retourne le nom du champion
            return name
    return False


# Definition de la fonction afficher_champions
def mastery_recap(summoner_name, champions_count):

    data_summoner = requests.get(
        f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
    ).json()

    if type(data_summoner) == dict and "status" in data_summoner:
        if 403 == data_summoner["status"]["status_code"]:
            print("API key expired.")
            exit()
        elif "id" not in data_summoner:
            print("Erreur, la requête n'a pas retourné d'id")
            exit()

    summoner_id = data_summoner.get("id")

    champions = requests.get(
        f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}?api_key={api_key}"
    ).json()

    if type(champions) == dict:
        if 403 == champions["status"]["status_code"]:
            print("API key expired.")
            exit()
    elif type(champions) != list:
        print("Erreur, la variable champions n'est pas une liste")
        exit()

    champions_data = []

    # On verifie que le nombre de champions demandé n'est pas superieur au nombre de champions du joueur
    # Si tel est le cas, on ne demande que le nombre de champions du joueur

    # len = length
    # len(champions) -> récupération de la longueur de la liste champions
    if champions_count > len(champions):
        champions_count = len(champions)

    for champion in champions[:int(champions_count)]:

        # On crée un dictionnaire pour stocker les données du champion
        champion_formatted_data = {}

        # On récupère le nom du champion à partir de son ID
        champion_name = get_champion_name_by_id(champion["championId"])

        # On vérifie si le nom du champion a été trouvé
        if champion_name == False:
            print("Champion's name not found")
            champion_formatted_data["name"] = champion["championId"]
        else:
            champion_formatted_data["name"] = champion_name

        # On ajoute les autres données du champion
        champion_formatted_data["points"] = champion["championPoints"]

        # On ajoute le dictionnaire du champion à la liste des champions
        champions_data.append(champion_formatted_data)

    champions_sorted_by_points = champions_data.copy()
    champions_sorted_by_points.sort(key=lambda champion: champion["points"], reverse=True)
    return(champions_sorted_by_points)
