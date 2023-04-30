# Importation du module requests
import requests

# Importation de la variable api_key du module app
from ..app import api_key

# Récupération de toutes les versions du jeu dans un dictionnaire
# Stockage de la première version de la liste (la plus récente) dans la variable version_patch
version_patch = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]

# Récupération des données des champions en français à partir de la dernière version du jeu
# Stockage des données des champions dans la variable data_full_champion
data_full_champion = requests.get(
    'https://ddragon.leagueoflegends.com/cdn/' + version_patch + '/data/fr_FR/champion.json').json()

# Stockage des données des champions dans la variable data_champion_by_name
data_champion_by_name = data_full_champion["data"]

# Définition de la fonction get_champion_name_by_id qui récupère le nom d'un champion à partir de son ID
def get_champion_name_by_id(id):
    # Utilisation de la variable globale data_champion_by_name
    global data_champion_by_name
    # Parcours de la liste des champions
    for name in data_champion_by_name:
        # Vérification si l'ID du champion correspond à l'ID du champion recherché
        if data_champion_by_name[name]['key'] == str(id):
            # Si c'est le cas, retourne le nom du champion
            return name
    # Si le nom du champion n'a pas été trouvé, retourne False
    return False

# Définition de la fonction afficher_champions
def mastery_recap(summoner_name, champions_count):
    # Récupération des données du joueur
    data_summoner = requests.get(
        f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
    ).json()

    # Vérification d'erreur avec les données du joueur
    if type(data_summoner) == dict and "status" in data_summoner:
        if 403 == data_summoner["status"]["status_code"]:
            print("API key expired.")
            exit()
        elif "id" not in data_summoner:
            print("Erreur, la requête n'a pas retourné d'id")
            exit()

    # Récupération de l'ID du joueur
    summoner_id = data_summoner.get("id")

    # Récupération des champions et de leur niveau pour le joueur donné
    champions = requests.get(
        f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}?api_key={api_key}"
    ).json()

    # Vérification d'erreur avec les données des champions du joueur
    if type(champions) == dict:
        if 403 == champions["status"]["status_code"]:
            print("API key expired.")
            exit()
    elif type(champions) != list:
        print("Erreur, la variable champions n'est pas une liste")
        exit()

    # Création d'une liste pour stocker les données des champions
    champions_data = []

    # Vérification si le nombre de champions demandé n'est pas supérieur au nombre de champions du joueur
    # Si tel est le cas, on ne demande que le nombre de champions du joueur
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
