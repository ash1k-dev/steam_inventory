from random import randrange
from time import sleep

import requests


from config import APIKEY


def get_time_in_games(steam_id):
    """Getting time in all games"""
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    request = requests.get(url, params={"key": APIKEY, "steamid": steam_id})
    games_list = request.json()["response"]["games"]
    time_into_games = {}
    for game in games_list:
        if game["playtime_forever"] == 0:
            time = 0
        else:
            time = round(game["playtime_forever"] / 60, 1)
        time_into_games[game["appid"]] = time
    return time_into_games


def get_game_cost(game_id):
    """Getting game cost"""
    try:
        url = "http://store.steampowered.com/api/appdetails"
        request = requests.get(url, params={"appids": game_id, "cc": "ru"})
        game_cost = request.json()[str(game_id)]["data"]["price_overview"][
            "final_formatted"
        ]
        game_cost = int(game_cost.split(",")[0])
    except Exception:
        game_cost = 0
    return game_cost


# print(get_game_cost(261550))


def get_game_name(game_id):
    """Getting game cost"""
    url = "http://store.steampowered.com/api/appdetails"
    request = requests.get(url, params={"appids": game_id, "cc": "ru"})
    game_name = request.json()[str(game_id)]["data"]["name"]
    return game_name


def get_steam_id(steam_id: str) -> int:
    """Name to id translation"""
    if steam_id.isdigit():
        return int(steam_id)
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    request = requests.get(
        url, params={"key": APIKEY, "vanityurl": steam_id, "url_type": 1}
    )
    user_id = request.json()["response"]["steamid"]
    return int(user_id)


def get_steam_name(steam_id):
    """Getting name from steam id"""
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    request = requests.get(
        url,
        params={
            "key": APIKEY,
            "steamids": int(steam_id),
        },
    )
    steam_name = request.json()["response"]["players"][0]["personaname"]
    return steam_name


def get_games_id(steam_id: int) -> dict:
    """Getting all games id"""
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    games_id_full = requests.get(
        url,
        params={
            "key": APIKEY,
            "steamid": steam_id,
            "include_appinfo": 1,
        },
    )
    games_id = {}
    for id in games_id_full.json()["response"]["games"]:
        games_id[id["appid"]] = id["name"]
    return games_id


def get_steam_inventory(steam_id: int, game_id: int = 730) -> dict:
    """Getting all inventory"""
    # steam_id = get_steam_id(steam_id)
    url = f"https://steamcommunity.com/inventory/{steam_id}/{game_id}/2"
    data = requests.get(url)
    return data.json()


def get_classid_list(items: dict) -> dict:
    """
    Getting classid list from inventory
    (for counting the number of items)
    """
    classid_names = {}
    for classid in items["assets"]:
        id = int(classid["classid"])
        if id in classid_names:
            classid_names[id]["amount"] += 1
        else:
            classid_names[id] = {"amount": 1}
    return classid_names


def get_items_list(items: dict) -> dict:
    """Getting items names from inventory"""
    market_names = {}
    for market_name in items["descriptions"]:
        # if (
        #     market_name["type"] != "Extraordinary Collectible"
        #     and "Graffiti" not in market_name["market_hash_name"]
        # ):
        name = market_name["market_hash_name"]
        appid = market_name["appid"]
        classid = market_name["classid"]
        market_names[classid] = {"name": name, "appid": appid}
    return market_names


def get_item_cost(name: str, game_id: int = 730, currency: int = 5) -> float:
    """Getting cost of item"""
    url = "http://steamcommunity.com//market/priceoverview"
    market_item = requests.get(
        url,
        params={"appid": game_id, "market_hash_name": name, "currency": currency},
    )
    cost = market_item.json()["lowest_price"].split()
    cost = int(float(cost[0].replace(",", ".")))
    return cost


def get_item_market_hash_name(item_id, app_id=730):
    url = f"https://api.steampowered.com/ISteamEconomy/GetAssetClassInfo/v1/"
    result = requests.get(
        url,
        params={"key": APIKEY, "appid": app_id, "class_count": 1, "classid0": item_id},
    )
    market_hash_name = result.json()["result"][str(item_id)]["market_hash_name"]
    return market_hash_name


def get_all_games_info(steam_id: int):
    final_list = {}
    games_id_list = get_games_id(steam_id)
    time_into_games = get_time_in_games(steam_id)
    for game_id, game_name in games_id_list.items():
        time = time_into_games[game_id]
        price = get_game_cost(game_id)
        final_list[game_id] = {"name": game_name, "time": time, "price": price}

    return final_list


def get_all_inventory_info(steam_id: int):
    # games_id_list = get_games_id(steam_id)
    # for game in games_id_list:
    #     steam_inventory = get_steam_inventory(user_id=int(steam_id), game_id=game)
    #     items_list = get_items_list(items=steam_inventory)
    #     classid_list = get_classid_list(items=steam_inventory)
    steam_inventory = get_steam_inventory(steam_id=steam_id, game_id=730)
    # classid_list = get_classid_list(items=steam_inventory)
    items_list = get_items_list(items=steam_inventory)
    for item, data in items_list.items():
        item_cost = get_item_cost(data["name"])
        items_list[item]["price"] = item_cost

    # return items_list, classid_list
    return items_list


def get_inventory_info_test_data(test_data):
    # steam_inventory = get_steam_inventory(steam_id=steam_id, game_id=730)
    steam_inventory = test_data
    classid_list = get_classid_list(items=steam_inventory)
    items_list = get_items_list(items=steam_inventory)
    for item, data in items_list.items():
        try:
            item_cost = get_item_cost(data["name"])
            items_list[item]["price"] = item_cost
            classid_list[int(item)]["first_cost"] = item_cost
        except Exception:
            # item_cost = randrange(10, 100)
            items_list[item]["price"] = 0
            classid_list[int(item)]["first_cost"] = 0
        sleep(randrange(4, 10))

    return items_list, classid_list
