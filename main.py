import json

import requests

"Получение списка игр"
from pprint import pprint

steamID = 76561198219397763
steamApiKey='3F61D3D434BDEC289A42F82B10A3776A'

# slink1 = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
# slink2 = "&steamid=" + steamID + "&include_appinfo=1&format=json"
# slink = slink1 + steamApiKey + slink2
#
# r = requests.get(slink)
#
# steam = r.json()
# pprint(steam)


def get_games_id(test_apikey, steamID):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    games_id_full = requests.get(url, params={
        'key': test_apikey,
        'steamid': steamID,
        'include_appinfo': 1,
    })
    games_id ={}
    for i in games_id_full.json()['response']['games']:
        games_id[i['appid']] = i['name']
    return games_id
    # return games_id_full.json()['response']['games']

a = get_games_id(steamApiKey, steamID)
pprint(a)


# "Получение id по нику"
# slink11 = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key=3F61D3D434BDEC289A42F82B10A3776A&vanityurl=denykill&url_type=1'
# r = requests.get(slink11)
#
# steam1 = r.json()
# pprint(steam1)


def get_steamid(user_id:str):
    url = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/'
    user_id = requests.get(url, params={
        'key': '3F61D3D434BDEC289A42F82B10A3776A',
        'vanityurl': user_id,
        'url_type': 1
    })
    return user_id


a = get_steamid('Denykill2')
print(a.json())