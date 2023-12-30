from random import randrange
from time import sleep

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config import STORAGE_TIME
from core.db.methods.request import (
    get_all_games_from_db,
    get_all_items_from_db,
    get_all_steam_ids_from_db,
    get_all_tracking_games_from_db,
    get_all_tracking_items_from_db,
    get_amount_and_items_info_from_db,
    get_games_from_db,
    get_games_info_from_db,
    get_items_info_from_db,
)
from core.inventory.steam import get_game_cost, get_item_cost


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


async def update_tracking_redis(session, tracking_type, user_telegram_id):
    tracking_type_dict = {
        "tracking_items": get_all_tracking_items_from_db,
        "tracking_games": get_all_tracking_games_from_db,
    }
    current_type_func = tracking_type_dict.get(tracking_type)
    all_items_or_games = await current_type_func(
        telegram_id=user_telegram_id, session=session
    )
    tracking_items_redis = {}
    for item in all_items_or_games:
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
        session=session, steam_id=steam_id, limit=1000
    )
    tracking_items_redis = {}
    for item in all_items:
        name, cost, first_cost, amount, difference = item
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
    all_items = await get_games_from_db(session=session, steam_id=steam_id)
    tracking_items_redis = {}
    for item in all_items:
        item_id, game_name, first_cost, time_in_game, cost = item
        difference = first_cost - cost
        tracking_items_redis.update(
            {
                f"{item_id}": {
                    "item_id": item_id,
                    "name": game_name,
                    "first_cost": first_cost,
                    "cost": cost,
                    "time": time_in_game,
                    "difference": difference,
                }
            }
        )
    return tracking_items_redis


async def update_items_info_redis(session, steam_id):
    items_data = await get_items_info_from_db(session=session, steam_id=steam_id)
    total_cost, first_total_cost, total_amount, max_cost, min_cost = items_data[0]
    items_info = {
        "total_cost": total_cost,
        "first_total_cost": first_total_cost,
        "total_amount": total_amount,
        "max_cost": max_cost,
        "min_cost": min_cost,
    }
    return items_info


async def update_games_info_redis(session, steam_id):
    games_data = await get_games_info_from_db(session=session, steam_id=steam_id)
    number_of_games, total_cost, time_in_games = games_data[0]
    games_info = {
        "number_of_games": number_of_games,
        "total_cost": total_cost,
        "time_in_games": time_in_games,
    }
    return games_info


async def update_redis(user_telegram_id, session: async_sessionmaker, storage):
    tracking_items = await update_tracking_redis(
        session=session,
        user_telegram_id=user_telegram_id,
        tracking_type="tracking_items",
    )
    tracking_games = await update_tracking_redis(
        session=session,
        user_telegram_id=user_telegram_id,
        tracking_type="tracking_games",
    )
    all_steam_ids = await get_all_steam_ids_from_db(
        telegram_id=user_telegram_id, session=session
    )
    all_items_and_games = {}
    all_items_and_games["ids"] = {steam_id: name for steam_id, name in all_steam_ids}
    for steam_id, _ in all_steam_ids:
        update_items_info = await update_items_info_redis(
            session=session, steam_id=steam_id
        )
        update_games_info = await update_games_info_redis(
            session=session, steam_id=steam_id
        )
        update_items = await update_items_redis(session=session, steam_id=steam_id)
        update_games = await update_games_redis(session=session, steam_id=steam_id)
        update_items_steam = {
            f"{steam_id}": {
                "items": update_items,
                "games": update_games,
                "items_info": update_items_info,
                "games_info": update_games_info,
            }
        }
        all_items_and_games.update(update_items_steam)

    user_data = {
        f"{user_telegram_id}": {
            "tracking_items": tracking_items,
            "tracking_games": tracking_games,
            "steam_ids": all_items_and_games,
        }
    }

    for key in user_data.keys():
        await storage.redis.set(key, str(user_data[key]), ex=STORAGE_TIME)
