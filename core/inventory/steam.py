import logging
from random import randrange
from time import sleep

import requests

from config import APIKEY, START_RANGE_SLEEP, STOP_RANGE_SLEEP


def get_game_cost(game_id):
    try:
        url = "http://store.steampowered.com/api/appdetails"
        request = requests.get(url, params={"appids": game_id, "cc": "ru"})
        game_cost = request.json()[str(game_id)]["data"]["price_overview"][
            "final_formatted"
        ]
        game_cost = game_cost.split()[0]
        if "," in game_cost:
            game_cost = int(game_cost.split(",")[0])
        else:
            game_cost = int(game_cost)
    except KeyError:
        logging.warning(msg=f"Not for sale now or zero cost: {game_id}")
        game_cost = 0
    return game_cost


def get_game_name(game_id):
    url = "http://store.steampowered.com/api/appdetails"
    request = requests.get(url, params={"appids": game_id, "cc": "ru"})
    game_name = request.json()[str(game_id)]["data"]["name"]
    return game_name


def get_steam_id(steam_id: str) -> int:
    if steam_id.isdigit():
        return int(steam_id)
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    request = requests.get(
        url, params={"key": APIKEY, "vanityurl": steam_id, "url_type": 1}
    )
    user_id = request.json()["response"]["steamid"]
    return int(user_id)


def get_steam_name(steam_id):
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


def get_games_info_without_cost(steam_id: int) -> dict:
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
        if id["playtime_forever"] == 0:
            time = 0
        else:
            time = round(id["playtime_forever"] / 60, 1)
        games_id[id["appid"]] = {
            "name": id["name"],
            "time": time,
        }
    return games_id


def get_steam_inventory(steam_id: int, game_id: int = 730) -> dict:
    # steam_id = get_steam_id(steam_id)
    url = f"https://steamcommunity.com/inventory/{steam_id}/{game_id}/2"
    data = requests.get(url)
    return data.json()


def get_classid_list(items: dict) -> dict:
    classid_names = {}
    for classid in items["assets"]:
        id = int(classid["classid"])
        if id in classid_names:
            classid_names[id]["amount"] += 1
        else:
            classid_names[id] = {"amount": 1}
    return classid_names


def get_items_list(items: dict) -> dict:
    market_names = {}
    for market_name in items["descriptions"]:
        name = market_name["market_hash_name"]
        appid = market_name["appid"]
        classid = market_name["classid"]
        market_names[classid] = {"name": name, "appid": appid}
    return market_names


def get_item_cost(name: str, game_id: int = 730, currency: int = 5) -> float:
    url = "http://steamcommunity.com//market/priceoverview"
    try:
        market_item = requests.get(
            url,
            params={"appid": game_id, "market_hash_name": name, "currency": currency},
        )
        cost = market_item.json()["lowest_price"].split()
        cost = round(float(cost[0].replace(",", ".")), 2)
        return cost
    except KeyError:
        logging.warning(f"Item - {name} has not price")


def get_item_market_hash_name(item_id, app_id=730):
    url = "https://api.steampowered.com/ISteamEconomy/GetAssetClassInfo/v1/"
    result = requests.get(
        url,
        params={"key": APIKEY, "appid": app_id, "class_count": 1, "classid0": item_id},
    )
    market_hash_name = result.json()["result"][str(item_id)]["market_hash_name"]
    return market_hash_name


def get_all_games_info(steam_id: int):
    final_list = {}
    games_id_list = get_games_info_without_cost(steam_id)
    for game_id, game_data in games_id_list.items():
        time = game_data["time"]
        price = get_game_cost(game_id)
        final_list[game_id] = {"name": game_data["name"], "time": time, "price": price}

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
    steam_inventory = test_data
    classid_list = get_classid_list(items=steam_inventory)
    items_list = get_items_list(items=steam_inventory)
    for item, data in items_list.items():
        try:
            item_cost = get_item_cost(data["name"])
            items_list[item]["price"] = item_cost
            classid_list[int(item)]["first_cost"] = item_cost
        except KeyError:
            logging.warning(msg=f"Zero price or no price: {data['name']}({item})")
        sleep(randrange(START_RANGE_SLEEP, STOP_RANGE_SLEEP))

    return items_list, classid_list
