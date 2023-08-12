import os
from random import randrange
from time import sleep

import requests
from dotenv import load_dotenv
from fake_useragent import UserAgent

load_dotenv()

apikey = os.getenv("APIKEY")
user_id = os.getenv("USER_ID")


ua = UserAgent()


def get_games_id(user_id:str | int):
    if type(user_id) is str:
        user_id = get_steam_id(user_id)
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    games_id_full = requests.get(url, params={
        'key': apikey,
        'steamid': user_id,
        'include_appinfo': 1,
    })
    games_id ={}
    for i in games_id_full.json()['response']['games']:
        games_id[i['appid']] = i['name']
    return games_id


def get_steam_id(user_id:str):
    url = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/'
    user_id = requests.get(url, params={
        'key': apikey,
        'vanityurl': user_id,
        'url_type': 1
    })
    return user_id


def get_steam_inventory(user_id:int|str, game_id:int=730):
    if type(user_id) is str:
        user_id = get_steam_id(user_id)
    address = f'https://steamcommunity.com/inventory/{user_id}/{game_id}/2'
    data = requests.get(address)
    return data.json()


def get_classid_list(items:dict):
    classid_names = []
    for classid in items["assets"]:
        id = classid["classid"]
        classid_names.append(id)
    return classid_names


def get_items_list(items:dict):
    market_names = {}
    for market_name in items["descriptions"]:
        if market_name["type"]!="Extraordinary Collectible" and "Graffiti" not in market_name["market_hash_name"]:
            item = market_name["market_hash_name"]
            appid = market_name["appid"]
            classid = market_name["classid"]
            market_names[item] = [appid, classid]
    return market_names


def get_item_cost(name:str, game_id:int=730, currency:int=5):
    url = 'http://steamcommunity.com//market/priceoverview'
    market_item = requests.get(url, params={
        'appid': game_id,
        'market_hash_name': name,
        'currency': currency
    }, headers={'user-agent': f'{ua.random}'})
    return market_item.json()['lowest_price']


test = get_steam_inventory(user_id=user_id)
items_list = get_items_list(items=test)
test_items_list = {}
test_inventory = []


for k, item in enumerate(items_list):
    test_inventory.append(item)

for k, item in enumerate(items_list):
    try:
        test_items_list[item] = get_item_cost(item)
        sleep(randrange(2, 10))
    except BaseException:
        pass


print(test_inventory)
print(len(test_inventory))

print(test_items_list)
print(len(test_items_list))

print(set(test_inventory).difference(test_items_list.keys()))


