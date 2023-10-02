from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.models import (  # SteamInventory,; SteamItem,; SteamItemsInInventory,
    Game,
    SteamId,
    User,
    SteamItem,
)

from core.db.methods.request import get_user_from_db


async def create_user(user_name: str, telegram_id: int, session: AsyncSession) -> None:
    """Creating user"""
    user = User(user_name=user_name, telegram_id=telegram_id)
    session.add(user)
    await session.commit()


async def create_steamid(steam_id, telegram_id, steam_name, session: AsyncSession):
    user = await get_user_from_db(telegram_id=telegram_id, session=session)
    steam_id = SteamId(steam_id=steam_id, user_id=user.id, steam_name=steam_name)
    session.add(steam_id)
    await session.commit()


# def create_steam_inventorys(games_list, previous_inventory_cost, now_inventory_cost):
#     all_inventorys = []
#     for game in games_list:
#         steam_inventory = SteamInventory(
#             games_id=game,
#             previous_inventory_cost=previous_inventory_cost,
#             now_inventory_cost=now_inventory_cost,
#         )
#         all_inventorys.append(steam_inventory)
#     session.add_all(all_inventorys)
#     session.commit()


def create_steam_items(
    items_list, name, app_id, classid, previous_item_cost, now_item_cost, session
):
    all_items = []
    for item in items_list:
        steam_item = SteamItem(
            name=name,
            app_id=app_id,
            classid=classid,
            previous_item_cost=previous_item_cost,
            now_item_cost=now_item_cost,
        )
        all_items.append(steam_item)
    session.add_all(all_items)
    session.commit()


#
#
# def create_steam_items_in_inventory(amount, inventory_id, item_id):
#     steam_items_in_inventory = SteamItemsInInventory(
#         amount=amount, inventory_id=inventory_id, item_id=item_id
#     )
#     session.add(steam_items_in_inventory)
#     session.commit()


async def create_game(game_name, game_id, game_cost, time_in_game, steam_id, session):
    game = Game(
        game_name=game_name,
        game_id=game_id,
        time_in_game=time_in_game,
        game_cost=game_cost,
        steam_id=steam_id,
    )
    session.add(game)
    await session.commit()
