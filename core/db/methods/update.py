from core.db.methods.request import (
    get_all_games_from_db,
    get_all_items_from_db,
    get_all_tracking_games_from_db,
)
from sqlalchemy.ext.asyncio import AsyncSession
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


async def method_name(user_telegram_id, session):
    all_tracking_games = await get_all_tracking_games_from_db(
        telegram_id=user_telegram_id, session=session
    )
    tracking_games_redis = {}
    tracking_games_redis[str(user_telegram_id)] = {}
    for tracking_game in all_tracking_games:
        _, name, game_id, first_game_cost, game_cost = tracking_game
        difference_for_tracking_games = first_game_cost - game_cost
        tracking_games_redis[str(user_telegram_id)][str(game_id)] = {}
        tracking_games_redis[str(user_telegram_id)][str(game_id)]["name"] = name
        tracking_games_redis[str(user_telegram_id)][str(game_id)][
            "first_game_cost"
        ] = first_game_cost
        tracking_games_redis[str(user_telegram_id)][str(game_id)][
            "game_cost"
        ] = game_cost
        tracking_games_redis[str(user_telegram_id)][str(game_id)][
            "difference_for_tracking_games"
        ] = difference_for_tracking_games
        for key in tracking_games_redis.keys():
            rs.set(key, str(tracking_games_redis[key]), ex=600)
