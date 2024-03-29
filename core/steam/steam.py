import logging
from random import randrange
from time import sleep

import requests

from config import (
    APIKEY,
    CURRENCY,
    FLOATING_POINT_VARIABLE,
    START_RANGE_SLEEP,
    STOP_RANGE_SLEEP,
)


def get_game_cost(game_id: int) -> float:
    """Получение стоимости игры"""
    try:
        url = "http://store.steampowered.com/api/appdetails"
        request = requests.get(url, params={"appids": game_id, "cc": "ru"})
        game_cost = request.json()[str(game_id)]["data"]["price_overview"][
            "final_formatted"
        ]
        game_cost = game_cost.split()[0]
        if "," in game_cost:
            game_cost = (
                round(float(game_cost.replace(",", ".")), 2) * FLOATING_POINT_VARIABLE
            )
        else:
            game_cost = int(game_cost) * FLOATING_POINT_VARIABLE
    except KeyError:
        logging.warning(msg=f"Not for sale now or zero cost: {game_id}")
        game_cost = 0
    return game_cost


def get_game_name(game_id: int) -> str:
    """Получение названия игры"""
    url = "http://store.steampowered.com/api/appdetails"
    request = requests.get(url, params={"appids": game_id, "cc": "ru"})
    game_name = request.json()[str(game_id)]["data"]["name"]
    return game_name


def get_steam_id(steam_id: str) -> int:
    """Получение Steam id"""
    if steam_id.isdigit():
        return int(steam_id)
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    request = requests.get(
        url, params={"key": APIKEY, "vanityurl": steam_id, "url_type": 1}
    )
    user_id = request.json()["response"]["steamid"]
    return int(user_id)


def get_steam_name(steam_id: int) -> str:
    """Получение имени пользователя в Steam"""
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


def get_steam_inventory(steam_id: int, game_id: int = 730) -> dict:
    """Получение инвентаря Steam"""
    url = f"https://steamcommunity.com/inventory/{steam_id}/{game_id}/2"
    data = requests.get(url)
    return data.json()


def get_item_cost(name: str, game_id: int = 730, currency: int = CURRENCY) -> float:
    """Получение стоимости предмета"""
    url = "http://steamcommunity.com//market/priceoverview"
    try:
        market_item = requests.get(
            url,
            params={"appid": game_id, "market_hash_name": name, "currency": currency},
        )
        cost = market_item.json()["lowest_price"].split()
        cost = round(float(cost[0].replace(",", ".")), 2) * FLOATING_POINT_VARIABLE
    except KeyError:
        logging.warning(f"Item - {name} has not price")
        cost = 0
    return cost


def get_item_market_hash_name(item_id: int, app_id: int = 730) -> str:
    """Получение названия предмета"""
    url = "https://api.steampowered.com/ISteamEconomy/GetAssetClassInfo/v1/"
    result = requests.get(
        url,
        params={"key": APIKEY, "appid": app_id, "class_count": 1, "classid0": item_id},
    )
    market_hash_name = result.json()["result"][str(item_id)]["market_hash_name"]
    return market_hash_name


def get_all_games_info(steam_id: int) -> dict:
    """Получение информации о всех играх пользователя Steam"""
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    game_ids = requests.get(
        url,
        params={
            "key": APIKEY,
            "steamid": steam_id,
            "include_appinfo": 1,
        },
    )
    games_info = {}
    for id in game_ids.json()["response"]["games"]:
        if id["playtime_forever"] == 0:
            time = 0
        else:
            time = round(id["playtime_forever"] / 60, 1)
        games_info[id["appid"]] = {
            "name": id["name"],
            "time": time,
            "cost": get_game_cost(id["appid"]),
        }
    return games_info


def get_all_items_info(items: dict) -> dict:
    """Получение информации о всех предметах"""
    items_info = {}
    for classid in items["assets"]:
        id = int(classid["classid"])
        if id in items_info:
            items_info[id]["amount"] += 1
        else:
            items_info[id] = {"amount": 1}
    for market_name in items["descriptions"]:
        name = market_name["market_hash_name"]
        item_cost = get_item_cost(name)
        appid = market_name["appid"]
        classid = int(market_name["classid"])
        items_info[classid].update({"name": name, "appid": appid, "cost": item_cost})
        sleep(randrange(START_RANGE_SLEEP, STOP_RANGE_SLEEP))
    return items_info
