import requests
from ..app import api_key

def API_check():
    data = requests.get('https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations?api_key=' + api_key).json()
    try:
        if data['status']['status_code'] != 200:
            return False
    except KeyError:
        return True
