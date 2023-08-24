from core.db.database import session
from core.db.models import (SteamId, SteamInventory, SteamItem,
                            SteamItemsInInventory, User)


def create_user(user_name, telegram_id):
    user = User(
        user_name = user_name,
        telegram_id =telegram_id
    )
    session.add(user)
    session.commit()


def create_steamid(steam_id, user_id):
    steam_id = SteamId(
        steam_id=steam_id,
        user_id = user_id
    )
    session.add(steam_id)
    session.commit()


def create_steam_inventorys(games_list, previous_inventory_cost,now_inventory_cost):
    all_inventorys = []
    for game in games_list:
        steam_inventory = SteamInventory(
            games_id=game,
            previous_inventory_cost = previous_inventory_cost,
            now_inventory_cost = now_inventory_cost
        )
        all_inventorys.append(steam_inventory)
    session.add_all(all_inventorys)
    session.commit()


def create_steam_items(items_list, name, app_id, classid, previous_item_cost, now_item_cost):
    all_items = []
    for item in items_list:
        steam_item = SteamItem(
            name=name,
            app_id = app_id,
            classid = classid,
            previous_item_cost = previous_item_cost,
            now_item_cost = now_item_cost
        )
        all_items.append(steam_item)
    session.add_all(all_items)
    session.commit()


def create_steam_items_in_inventory(amount, inventory_id, item_id):
    steam_items_in_inventory = SteamItemsInInventory(
        amount=amount,
        inventory_id = inventory_id,
        item_id = item_id
    )
    session.add(steam_items_in_inventory)
    session.commit()
