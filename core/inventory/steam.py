import requests
from fake_useragent import UserAgent

ua = UserAgent()


def get_steam_inventory(user_id:int|str, game_id:int=730):
    if type(user_id) is str:
        pass
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
        if market_name["type"]!="Extraordinary Collectible":
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


test_id = 76561198155948643

test = get_steam_inventory(user_id=test_id)
items_list = get_items_list(items=test)
inventory_cost = 0
for item in items_list:
    print(item, get_item_cost(item))

