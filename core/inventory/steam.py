from random import randrange
from time import sleep

import requests
from fake_useragent import UserAgent

from config import APIKEY

ua = UserAgent()


def get_games_id(user_id:str | int) -> dict:
    """geting all games id"""
    if type(user_id) is str:
        user_id = get_steam_id(user_id)
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    games_id_full = requests.get(url, params={
        'key': APIKEY,
        'steamid': user_id,
        'include_appinfo': 1,
    })
    games_id ={}
    for id in games_id_full.json()['response']['games']:
        games_id[id['appid']] = id['name']
    return games_id


def get_steam_id(user_id:str) -> int:
    """name to id translation"""
    url = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/'
    user_id = requests.get(url, params={
        'key': APIKEY,
        'vanityurl': user_id,
        'url_type': 1
    })
    return user_id


def get_steam_inventory(user_id:int|str, game_id:int=730) -> dict:
    """geting all inventory"""
    if type(user_id) is str:
        user_id = get_steam_id(user_id)
    address = f'https://steamcommunity.com/inventory/{user_id}/{game_id}/2'
    data = requests.get(address)
    return data.json()


def get_classid_list(items:dict) -> dict:
    """
    geting classid list from inventory
    (for counting the number of items)
    """
    classid_names = {}
    for classid in items["assets"]:
        id = classid["classid"]
        if classid_names[id] in classid_names:
            classid_names[id]+=1
        else:
            classid_names[id]=1
    return classid_names


def get_items_list(items:dict) -> dict:
    """geting items names from inventory"""
    market_names = {}
    for market_name in items["descriptions"]:
        if market_name["type"]!="Extraordinary Collectible" and "Graffiti" not in market_name["market_hash_name"]:
            item = market_name["market_hash_name"]
            appid = market_name["appid"]
            classid = market_name["classid"]
            market_names[item] = [appid, classid]
    return market_names


def get_item_cost(name:str, game_id:int=730, currency:int=5) -> float:
    """geting cost of item"""
    url = 'http://steamcommunity.com//market/priceoverview'
    market_item = requests.get(url, params={
        'appid': game_id,
        'market_hash_name': name,
        'currency': currency
    }, headers={'user-agent': f'{ua.random}'})
    cost = market_item.json()['lowest_price'].split()
    cost = float(cost[0].replace(',', '.'))
    return cost


def all_test(user_id: str | int) -> None:
    games_id_list = get_games_id(user_id)
    for game in games_id_list:
        steam_inventory = get_steam_inventory(user_id=int(user_id), game_id=game)
        items_list = get_items_list(items=steam_inventory)
        classid_list = get_classid_list(items=steam_inventory)


    test_items_list = {}
    test_inventory_cost = 0
    for k, item in enumerate(items_list):
        try:
            cost = get_item_cost(item)
            test_items_list[item] = cost
            test_inventory_cost += cost
            sleep(randrange(3, 10))
        except BaseException:
            pass
    return test_inventory_cost
