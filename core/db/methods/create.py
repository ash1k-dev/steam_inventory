from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.models import (
    Game,
    GameInAccount,
    SteamId,
    User,
    SteamInventory,
    SteamItemsInInventory,
    SteamItem,
)

from core.db.methods.request import (
    get_user_from_db,
    get_items_list_from_db,
    get_games_list_from_db,
    get_steamid_from_db,
    get_inventorys_id_from_db,
)
from core.inventory.steam import get_all_games_info, get_inventory_info_test_data
from core.inventory.test_data import inventory_json


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
    items_list = await get_items_list_from_db(session=session)
    for item_id, item_data in items_dict.items():
        if int(item_id) not in items_list:
            steam_item = SteamItem(
                name=item_data["name"],
                app_id=item_data["appid"],
                classid=int(item_id),
                # first_item_cost=item_data["price"],
                item_cost=item_data["price"],
            )
            items.append(steam_item)
    session.add_all(items)
    await session.commit()


async def create_steam_items_in_inventory(
    classid_dict: dict, inventory_id: int, session: AsyncSession
):
    classids = []
    for classid, data in classid_dict.items():
        steam_items_in_inventory = SteamItemsInInventory(
            amount=data["amount"],
            inventory_id=inventory_id,
            item_id=classid,
            first_item_cost=data["first_cost"],
        )
        classids.append(steam_items_in_inventory)
    session.add_all(classids)
    await session.commit()


async def create_all_games(
    all_games_info: dict, steam_id: int, session: AsyncSession
) -> None:
    all_games = []
    games_list = await get_games_list_from_db(session=session)
    for game_id, game_data in all_games_info.items():
        if game_id not in games_list:
            game = Game(
                game_id=game_id,
                game_name=game_data["name"],
                game_cost=game_data["price"],
            )
            all_games.append(game)
        game_in_account = GameInAccount(
            game_id=game_id,
            game_name=game_data["name"],
            first_game_cost=game_data["price"],
            time_in_game=game_data["time"],
            steam_id=steam_id,
        )
        all_games.append(game_in_account)
    session.add_all(all_games)
    await session.commit()


# async def create_all_games(
#     all_games_info: dict, steam_id: int, session: AsyncSession
# ) -> None:
#     all_games = []
#     for game_id, game_data in all_games_info.items():
#         game = Game(
#             game_id=game_id,
#             game_name=game_data["name"],
#             game_cost=game_data["price"],
#             time_in_game=game_data["time"],
#             steam_id=steam_id,
#         )
#         all_games.append(game)
#     session.add_all(all_games)
#     await session.commit()


# async def create_games_in_account(
#     classid_dict: dict, inventory_id: int, session: AsyncSession
# ):
#     classids = []
#     for classid, amount in classid_dict.items():
#         steam_items_in_inventory = SteamItemsInInventory(
#             amount=amount, inventory_id=inventory_id, item_id=classid
#         )
#         classids.append(steam_items_in_inventory)
#     session.add_all(classids)
#     await session.commit()


async def add_initial_data(message, session, steam_id, steam_name):
    await create_steamid(
        telegram_id=message.from_user.id,
        steam_id=steam_id,
        steam_name=steam_name,
        session=session,
    )
    all_games_info = get_all_games_info(steam_id=steam_id)
    steam_id_from_db = await get_steamid_from_db(steam_id, session=session)
    await create_all_games(
        all_games_info=all_games_info,
        steam_id=steam_id_from_db.id,
        session=session,
    )
    await create_all_steam_inventorys(
        all_games_info=all_games_info,
        steam_id=steam_id_from_db.id,
        session=session,
    )
    items_dict, classid_dict = get_inventory_info_test_data(inventory_json)
    await create_all_steam_items(items_dict, session=session)
    inventorys_id = await get_inventorys_id_from_db(
        session=session, steam_id=steam_id_from_db.id
    )
    await create_steam_items_in_inventory(
        classid_dict, inventory_id=inventorys_id.id, session=session
    )
