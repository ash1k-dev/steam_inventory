from sqlalchemy.ext.asyncio import AsyncSession

from core.db.methods.request import (
    get_game_from_db,
    get_games_list_from_db,
    get_inventorys_id_from_db,
    get_item_from_db,
    get_items_list_from_db,
    get_steamid_from_db,
)
from core.db.models.models import (
    Game,
    GameInAccount,
    GameTrack,
    Inventory,
    Item,
    ItemInInventory,
    ItemTrack,
    Steam,
    User,
)
from core.steam.steam import (
    get_all_games_info,
    get_game_cost,
    get_game_name,
    get_inventory_info,
    get_item_cost,
    get_item_market_hash_name,
)
from core.steam.test_data import inventory_json


async def create_user(name: str, telegram_id: int, session: AsyncSession) -> None:
    user = User(name=name, telegram_id=telegram_id)
    session.add(user)
    await session.commit()


async def create_steam(
    steam_id: int, telegram_id: int, steam_name: str, session: AsyncSession
) -> None:
    steam_id = Steam(steam_id=steam_id, user_id=telegram_id, name=steam_name)
    session.add(steam_id)
    await session.commit()


async def create_all_steam_inventorys(
    all_games_info: dict, steam_id: int, session: AsyncSession
):
    all_inventory = []
    for game_id in all_games_info:
        steam_inventory = Inventory(
            steam_id=steam_id,
            games_id=game_id,
        )
        all_inventory.append(steam_inventory)
    session.add_all(all_inventory)
    await session.commit()


async def create_all_steam_items(items_data: dict, session: AsyncSession) -> None:
    items = []
    items_list = await get_items_list_from_db(session=session)
    for item_id, item_data in items_data.items():
        if int(item_id) not in items_list:
            steam_item = Item(
                name=item_data["name"],
                app_id=item_data["appid"],
                classid=item_id,
                cost=item_data["cost"],
            )
            items.append(steam_item)
    session.add_all(items)
    await session.commit()


async def create_steam_items_in_inventory(
    items_data: dict, inventory_id: int, session: AsyncSession
):
    classids = []
    for classid, data in items_data.items():
        steam_items_in_inventory = ItemInInventory(
            amount=data["amount"],
            inventory_id=inventory_id,
            item_id=classid,
            first_cost=data["cost"],
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
                name=game_data["name"],
                cost=game_data["cost"],
            )
            all_games.append(game)
        game_in_account = GameInAccount(
            game_id=game_id,
            game_name=game_data["name"],
            first_cost=game_data["cost"],
            time_in_game=game_data["time"],
            steam_id=steam_id,
        )
        all_games.append(game_in_account)
    session.add_all(all_games)
    await session.commit()


async def create_all_items(
    all_items_info: dict, inventory_id: int, session: AsyncSession
) -> None:
    all_items = []
    items_list = await get_items_list_from_db(session=session)
    for item_id, item_data in all_items_info.items():
        if item_id not in items_list and item_data["cost"] != 0:
            steam_item = Item(
                name=item_data["name"],
                app_id=item_data["appid"],
                classid=item_id,
                cost=item_data["cost"],
            )
            all_items.append(steam_item)
    for item_id, item_data in all_items_info.items():
        if item_data["cost"] != 0:
            steam_items_in_inventory = ItemInInventory(
                amount=item_data["amount"],
                inventory_id=inventory_id,
                item_id=item_id,
                first_cost=item_data["cost"],
            )
            all_items.append(steam_items_in_inventory)
    session.add_all(all_items)
    await session.commit()


async def add_initial_data(message, session, steam_id, steam_name):
    await create_steam(
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
    """This is where the code is for getting all the items from each specific game"""
    # for game_id in all_games_info.keys():
    #     inventory_game_data = get_steam_inventory(steam_id=steam_id, game_id=game_id)
    #     all_items_info = get_inventory_info(inventory_game_data)
    #     inventory_id = await get_inventorys_id_from_db(
    #         session=session, steam_id=steam_id_from_db.id
    #     )
    #     await create_all_items(all_items_info, inventory_id=inventory_id.id, session=session)

    """This is where the code is for getting items for a specific game with test data"""
    inventory_id = await get_inventorys_id_from_db(
        session=session, steam_id=steam_id_from_db.id
    )
    all_items_info = get_inventory_info(inventory_json)
    await create_all_items(
        all_items_info, inventory_id=inventory_id.id, session=session
    )


async def create_game(
    game_id: int, game_name, game_cost, session: AsyncSession
) -> None:
    game = Game(name=game_name, game_id=game_id, cost=game_cost)
    session.add(game)
    await session.commit()


async def create_game_track(
    game_id: int, telegram_id: int, session: AsyncSession
) -> None:
    first_game_cost = get_game_cost(game_id=game_id)
    name = get_game_name(game_id=int(game_id))
    check_game = await get_game_from_db(game_id=game_id, session=session)
    if check_game is None:
        await create_game(
            game_name=name, game_id=game_id, game_cost=first_game_cost, session=session
        )
    game_track = GameTrack(
        name=name, first_cost=first_game_cost, user_id=telegram_id, game_id=game_id
    )
    session.add(game_track)
    await session.commit()


async def create_item(
    name: str, item_id: int, item_cost, session: AsyncSession
) -> None:
    game = Item(name=name, classid=item_id, cost=item_cost)
    session.add(game)
    await session.commit()


async def create_item_track(
    item_id: int, telegram_id: int, session: AsyncSession
) -> None:
    market_hash_name = get_item_market_hash_name(item_id=item_id)
    first_item_cost = get_item_cost(name=market_hash_name)
    check_item = await get_item_from_db(item_id=item_id, session=session)
    if check_item is None:
        await create_item(
            name=market_hash_name,
            item_id=item_id,
            item_cost=first_item_cost,
            session=session,
        )
    game_track = ItemTrack(
        name=market_hash_name,
        first_cost=first_item_cost,
        user_id=telegram_id,
        item_id=item_id,
    )
    session.add(game_track)
    await session.commit()
