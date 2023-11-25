from core.db.methods.request import (
    get_all_games_from_db,
    get_all_items_from_db,
)
from sqlalchemy.ext.asyncio import AsyncSession
from core.inventory.steam import get_item_cost, get_game_cost
from time import sleep
from random import randrange


async def update_all_items(session: AsyncSession):
    new_items_list = []
    items_list = await get_all_items_from_db(session=session)
    for item in items_list:
        try:
            new_item_cost = get_item_cost(item.name)
            if item.item_cost != new_item_cost:
                item.item_cost = new_item_cost
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
            if new_game_cost != game.game_cost:
                game.game_cost = new_game_cost
                new_items_list.append(game)
        except Exception:
            pass
        sleep(randrange(4, 10))
    session.add_all(new_items_list)
    await session.commit()
