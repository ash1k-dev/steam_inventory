from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.models import (
    Game,
    SteamId,
    User,
    SteamInventory,
    SteamItemsInInventory,
    SteamItem,
)

from core.db.methods.request import get_user_from_db


async def create_user(user_name: str, telegram_id: int, session: AsyncSession) -> None:
    """Creating user"""
    user = User(user_name=user_name, telegram_id=telegram_id)
    session.add(user)
    await session.commit()


async def create_steamid(
    steam_id: int, telegram_id: int, steam_name: str, session: AsyncSession
) -> None:
    user = await get_user_from_db(telegram_id=telegram_id, session=session)
    steam_id = SteamId(steam_id=steam_id, user_id=user.id, steam_name=steam_name)
    session.add(steam_id)
    await session.commit()


async def create_all_steam_inventorys(
    all_games_info: dict, steam_id: int, session: AsyncSession
):
    all_inventorys = []
    for game_id in all_games_info:
        steam_inventory = SteamInventory(
            steam_id=steam_id,
            games_id=game_id,
        )
        all_inventorys.append(steam_inventory)
    session.add_all(all_inventorys)
    await session.commit()


async def create_all_steam_items(items_dict: dict, session: AsyncSession) -> None:
    items = []
    for item_id, item_data in items_dict.items():
        steam_item = SteamItem(
            name=item_data["name"],
            app_id=item_data["appid"],
            classid=int(item_id),
            first_item_cost=item_data["price"],
            item_cost=item_data["price"],
        )
        items.append(steam_item)
    session.add_all(items)
    await session.commit()


async def create_steam_items_in_inventory(
    classid_dict: dict, inventory_id: int, session: AsyncSession
):
    classids = []
    for classid, amount in classid_dict.items():
        steam_items_in_inventory = SteamItemsInInventory(
            amount=amount, inventory_id=inventory_id, item_id=classid
        )
        classids.append(steam_items_in_inventory)
    session.add_all(classids)
    await session.commit()


async def create_all_games(
    all_games_info: dict, steam_id: int, session: AsyncSession
) -> None:
    all_games = []
    for game_id, game_data in all_games_info.items():
        game = Game(
            game_id=game_id,
            game_name=game_data["name"],
            game_cost=game_data["price"],
            time_in_game=game_data["time"],
            steam_id=steam_id,
        )
        all_games.append(game)
    session.add_all(all_games)
    await session.commit()
