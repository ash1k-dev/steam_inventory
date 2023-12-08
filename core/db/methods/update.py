from core.db.methods.request import (
    get_all_games_from_db,
    get_all_items_from_db,
    get_all_tracking_games_from_db,
    get_all_tracking_items_from_db,
    get_amount_and_items_info_from_db,
    get_top_games_from_db,
    get_all_steam_ids_from_db,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from core.inventory.steam import get_item_cost, get_game_cost
from time import sleep
from random import randrange

import redis

rs = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)


async def update_all_items(session: AsyncSession):
    new_items_list = []
    items_list = await get_all_items_from_db(session=session)
    for item in items_list:
        try:
            new_item_cost = get_item_cost(item.name)
            if item.cost != new_item_cost:
                item.cost = new_item_cost
                new_items_list.append(item)
        except Exception:
            pass
        sleep(randrange(4, 10))
    session.add_all(new_items_list)
    await session.commit()


async def update_all_games(session: AsyncSession):
    new_items_list = []
    all_games = await get_all_games_from_db(session=session)
    for game in all_games:
        try:
            new_game_cost = get_game_cost(game_id=game.game_id)
            if new_game_cost != game.cost:
                game.cost = new_game_cost
                new_items_list.append(game)
        except Exception:
            pass
        sleep(randrange(1, 3))
    session.add_all(new_items_list)
    await session.commit()


async def update_all_items_and_games(session):
    await update_all_items(session=session)
    await update_all_games(session=session)


async def update_tracking_redis(session, type_item, user_telegram_id=0):
    if type_item == "tracking_items":
        all_items = await get_all_tracking_items_from_db(
            telegram_id=user_telegram_id, session=session
        )
    elif type_item == "tracking_games":
        all_items = await get_all_tracking_games_from_db(
            telegram_id=user_telegram_id, session=session
        )
    tracking_items_redis = {}
    for item in all_items:
        name, item_id, first_cost, cost = item
        difference = first_cost - cost
        tracking_items_redis.update(
            {
                f"{item_id}": {
                    "name": name,
                    "first_cost": first_cost,
                    "cost": cost,
                    "difference": difference,
                }
            }
        )
    return tracking_items_redis


async def update_items_redis(session, steam_id):
    all_items = await get_amount_and_items_info_from_db(
        session=session, steam_id=steam_id
    )
    tracking_items_redis = {}
    for item in all_items:
        name, cost, first_cost, amount = item
        difference = first_cost - cost
        tracking_items_redis.update(
            {
                f"{name}": {
                    "name": name,
                    "first_cost": first_cost,
                    "cost": cost,
                    "amount": amount,
                    "difference": difference,
                }
            }
        )
    return tracking_items_redis


async def update_games_redis(session, steam_id):
    all_items = await get_top_games_from_db(session=session, steam_id=steam_id)
    tracking_items_redis = {}
    for item in all_items:
        item_id, game_name, first_cost, time_in_game, cost = item
        difference = first_cost - cost
        tracking_items_redis.update(
            {
                f"{item_id}": {
                    "name": game_name,
                    "first_cost": first_cost,
                    "cost": cost,
                    "time_in_game": time_in_game,
                    "difference": difference,
                }
            }
        )
    return tracking_items_redis


async def update_redis(user_telegram_id, session: async_sessionmaker):
    tracking_items = await update_tracking_redis(
        session=session,
        user_telegram_id=user_telegram_id,
        type_item="tracking_items",
    )
    tracking_games = await update_tracking_redis(
        session=session,
        user_telegram_id=user_telegram_id,
        type_item="tracking_games",
    )
    all_steam_ids = await get_all_steam_ids_from_db(
        telegram_id=user_telegram_id, session=session
    )
    update_items = {}
    for steam_id in all_steam_ids:
        update_items_st = await update_items_redis(
            session=session, steam_id=steam_id.steam_id
        )
        update_games_st = await update_games_redis(
            session=session, steam_id=steam_id.steam_id
        )
        update_items_steam = {
            f"{steam_id.steam_id}": {
                "update_items": update_items_st,
                "update_games": update_games_st,
            }
        }
        update_items.update(update_items_steam)

    user_data = {
        f"{user_telegram_id}": {
            "tracking_items": tracking_items,
            "tracking_games": tracking_games,
            "steam_id": update_items,
        }
    }

    for key in user_data.keys():
        rs.set(key, str(user_data[key]), ex=6000)
