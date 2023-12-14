from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import DEPRECIATION_FACTOR, INCREASE_FACTOR
from core.bot.keyboards.inline.callback_factory import GamesCallbackFactory
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
from redis_data_convert import redis_convert_to_dict


async def get_user_from_db(telegram_id: int, session: AsyncSession):
    """Getting a user from the database"""
    statement = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_all_user_from_db(session: AsyncSession):
    """Getting all users from the database"""
    statement = select(User)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_steamid_from_db(steam_id: int, session: AsyncSession):
    statement = select(Steam).where(Steam.steam_id == steam_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_all_steam_ids_from_db(telegram_id: int, session: AsyncSession):
    """Getting all steam ids from the database"""
    statement = select(Steam.steam_id, Steam.name).where(Steam.user_id == telegram_id)
    result = await session.execute(statement)
    return result.all()


#
async def get_games_from_db(
    steam_id: int,
    session: AsyncSession,
    limit: int = 1000,
    order: str = "all",
):
    """Getting games from the database"""
    if order == "time":
        order = GameInAccount.time_in_game
    elif order == "cost":
        order = Game.cost
    elif order == "all":
        order = GameInAccount.time_in_game
    steam_id = await get_steamid_from_db(steam_id=steam_id, session=session)
    statement = (
        select(
            GameInAccount.game_id,
            GameInAccount.game_name,
            GameInAccount.first_cost,
            GameInAccount.time_in_game,
            Game.cost,
        )
        .join(Game, Game.game_id == GameInAccount.game_id)
        .where(GameInAccount.steam_id == steam_id.id)
        .limit(limit)
        .order_by(desc(order))
    )
    result = await session.execute(statement)
    return result.all()


async def get_games_info_from_db(
    session: AsyncSession,
    steam_id,
):
    steamid_from_db = await get_steamid_from_db(steam_id=steam_id, session=session)
    statement = (
        select(
            func.count(
                GameInAccount.game_name,
            ),
            func.sum(Game.cost),
            func.sum(
                GameInAccount.time_in_game,
            ),
        )
        .join(Game, Game.game_id == GameInAccount.game_id)
        .where(GameInAccount.steam_id == steamid_from_db.id)
    )
    result = await session.execute(statement)
    return result.all()


async def get_inventorys_id_from_db(steam_id, session: AsyncSession):
    statement = select(Inventory).filter(
        Inventory.steam_id == steam_id, Inventory.games_id == 730
    )
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_items_info_from_db(
    session: AsyncSession,
    steam_id,
):
    steamid_from_db = await get_steamid_from_db(steam_id=steam_id, session=session)
    inventory_id = await get_inventorys_id_from_db(
        session=session, steam_id=steamid_from_db.id
    )
    statement = (
        select(
            func.sum(Item.cost),
            func.sum(ItemInInventory.first_cost),
            func.sum(ItemInInventory.amount),
            func.max(Item.cost),
            func.min(Item.cost),
        )
        .join(Item, Item.classid == ItemInInventory.item_id)
        .where(ItemInInventory.inventory_id == inventory_id.id)
    )
    result = await session.execute(statement)
    return result.all()


async def get_amount_and_items_info_from_db(
    session: AsyncSession, steam_id, order="all", limit=5
):
    if order == "all":
        order = Item.cost
        limit = 10000
    elif order == "top_cost":
        order = Item.cost
    elif order == "top_gain":
        order = "difference"
    steamid_from_db = await get_steamid_from_db(steam_id=steam_id, session=session)
    inventory_id = await get_inventorys_id_from_db(
        session=session, steam_id=steamid_from_db.id
    )
    statement = (
        select(
            Item.name,
            Item.cost,
            ItemInInventory.first_cost,
            ItemInInventory.amount,
            (Item.cost - ItemInInventory.first_cost).label("difference"),
        )
        .join(Item, Item.classid == ItemInInventory.item_id)
        .where(ItemInInventory.inventory_id == inventory_id.id)
        .order_by(desc(order))
        .limit(limit)
    )
    result = await session.execute(statement)
    return result.all()


async def get_items_list_from_db(
    session: AsyncSession,
):
    statement = select(Item.classid)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_games_list_from_db(
    session: AsyncSession,
):
    statement = select(Game.game_id)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_all_tracking_items_from_db(telegram_id: int, session: AsyncSession):
    """Getting all tracking items from the database"""
    statement = (
        select(
            ItemTrack.name,
            ItemTrack.item_id,
            ItemTrack.first_cost,
            Item.cost,
        )
        .join(Item, ItemTrack.item_id == Item.classid)
        .where(ItemTrack.user_id == telegram_id)
    )
    result = await session.execute(statement)
    return result.all()


async def get_all_tracking_games_from_db(telegram_id: int, session: AsyncSession):
    """Getting all tracking games from the database"""
    statement = (
        select(
            GameTrack.name,
            GameTrack.game_id,
            GameTrack.first_cost,
            Game.cost,
        )
        .join(Game, Game.game_id == GameTrack.game_id)
        .where(GameTrack.user_id == telegram_id)
    )
    result = await session.execute(statement)
    return result.all()


async def get_tracking_game_from_db(game_id: int, session: AsyncSession):
    """Getting all steam ids from the database"""
    statement = select(GameTrack).where(GameTrack.game_id == game_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_game_from_db(game_id: int, session: AsyncSession):
    statement = select(Game).where(Game.game_id == game_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_tracking_item_from_db(item_id: int, session: AsyncSession):
    """Getting all steam ids from the database"""
    statement = select(ItemTrack).where(ItemTrack.item_id == item_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_tracking_item_data_from_db(item_id: int, session: AsyncSession):
    """Getting all steam ids from the database"""
    statement = (
        select(ItemTrack.name, ItemTrack.first_cost, Item.cost)
        .join(Item, ItemTrack.item_id == Item.classid)
        .where(ItemTrack.item_id == item_id)
    )
    result = await session.execute(statement)
    return result.all()


async def get_tracking_game_data_from_db(game_id: int, session: AsyncSession):
    """Getting all steam ids from the database"""
    statement = (
        select(GameTrack.name, GameTrack.first_cost, Game.cost)
        .join(Game, GameTrack.game_id == Game.game_id)
        .where(GameTrack.game_id == game_id)
    )
    result = await session.execute(statement)
    return result.all()


async def get_item_from_db(item_id: int, session: AsyncSession):
    statement = select(Item).where(Item.classid == item_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_all_items_from_db(session: AsyncSession):
    statement = select(Item)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_all_games_from_db(session: AsyncSession):
    statement = select(Game)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_items_changes(session, user_telegram_id):
    all_steam_ids = await get_all_steam_ids_from_db(
        telegram_id=user_telegram_id, session=session
    )
    items = {}
    for steam_id in all_steam_ids:
        items_info = await get_amount_and_items_info_from_db(
            steam_id=steam_id.steam_id, session=session
        )
        items[f"{steam_id.steam_id}"] = []
        for item in items_info:
            name, item_cost, first_item_cost, _, _ = item
            if item_cost > first_item_cost * float(INCREASE_FACTOR):
                items[f"{steam_id.steam_id}"].append((name, item_cost, first_item_cost))
    return items


async def get_tracking_items_changes(session, user_telegram_id):
    all_tracking_items = await get_all_tracking_items_from_db(
        telegram_id=user_telegram_id, session=session
    )
    tracking_items = []
    for tracking_item in all_tracking_items:
        name, item_id, first_item_cost, item_cost = tracking_item
        if item_cost < first_item_cost * float(DEPRECIATION_FACTOR):
            tracking_items.append((name, item_id, first_item_cost, item_cost))
    return tracking_items


async def get_tracking_games_changes(user_telegram_id, session):
    all_tracking_games = await get_all_tracking_games_from_db(
        telegram_id=user_telegram_id, session=session
    )
    tracking_games = []
    for tracking_game in all_tracking_games:
        name, game_id, first_game_cost, game_cost = tracking_game
        if game_cost < first_game_cost * float(DEPRECIATION_FACTOR):
            tracking_games.append((name, game_id, first_game_cost, game_cost))
    return tracking_games


async def get_changes(user_telegram_id, session):
    items_changes = await get_items_changes(
        user_telegram_id=user_telegram_id, session=session
    )
    get_tracking_items = await get_tracking_items_changes(
        user_telegram_id=user_telegram_id, session=session
    )
    get_tracking_games = await get_tracking_games_changes(
        user_telegram_id=user_telegram_id,
        session=session,
    )
    return get_tracking_items, get_tracking_games, items_changes


async def get_items_list_from_redis_or_db(
    callback_data, session, telegram_id, storage, order
):
    user_data = await redis_convert_to_dict(telegram_id=telegram_id, storage=storage)
    if user_data:
        all_items = []
        items = user_data["steam_ids"][f"{callback_data.steam_id}"]["items"]
        items = [items_data for items_data in items.values()]
        items = sorted(items, key=lambda x: x[order], reverse=True)
        for item in items[: callback_data.limit]:
            name = item["name"]
            cost = item["cost"]
            first_cost = item["first_cost"]
            amount = item["amount"]
            difference = item["difference"]
            all_items.append((name, cost, first_cost, amount, difference))
    else:
        all_items = await get_amount_and_items_info_from_db(
            steam_id=callback_data.steam_id,
            limit=callback_data.limit,
            order=order,
            session=session,
        )
    return all_items


async def get_items_info_from_redis_or_db(session, callback_data, telegram_id, storage):
    user_data = await redis_convert_to_dict(telegram_id=telegram_id, storage=storage)
    if user_data:
        items_info = user_data["steam_ids"][f"{callback_data.steam_id}"]["items_info"]
        total_cost = items_info["total_cost"]
        first_total_cost = items_info["first_total_cost"]
        total_amount = items_info["total_amount"]
        max_cost = items_info["max_cost"]
        min_cost = items_info["min_cost"]
        difference_total_cost = total_cost - first_total_cost
    else:
        general_items_info = await get_items_info_from_db(
            steam_id=callback_data.steam_id, session=session
        )
        (
            total_cost,
            first_total_cost,
            total_amount,
            max_cost,
            min_cost,
        ) = general_items_info[0]
        difference_total_cost = total_cost - first_total_cost
    return (
        difference_total_cost,
        first_total_cost,
        max_cost,
        min_cost,
        total_amount,
        total_cost,
    )


async def get_games_info_from_redis_or_db(
    callback_data: GamesCallbackFactory,
    session: AsyncSession,
    telegram_id: int,
    storage: RedisStorage,
) -> tuple:
    user_data = await redis_convert_to_dict(
        telegram_id=f"{telegram_id}", storage=storage
    )
    if user_data:
        games_info = user_data["steam_ids"][f"{callback_data.steam_id}"]["games_info"]
        number_of_games = games_info["number_of_games"]
        total_cost = games_info["total_cost"]
        time_in_games = games_info["time_in_games"]
    else:
        general_games_info = await get_games_info_from_db(
            steam_id=callback_data.steam_id, session=session
        )
        number_of_games, total_cost, time_in_games = general_games_info[0]
    return number_of_games, time_in_games, total_cost


async def get_games_list_from_redis_or_db(
    callback_data: GamesCallbackFactory,
    session: AsyncSession,
    telegram_id: int,
    storage: RedisStorage,
    order: str,
) -> list[tuple]:
    user_data = await redis_convert_to_dict(
        telegram_id=f"{telegram_id}", storage=storage
    )
    if user_data:
        games_list = []
        games = user_data["steam_ids"][f"{callback_data.steam_id}"]["games"]
        games = [game_data for game_data in games.values()]
        games = sorted(games, key=lambda x: x[order], reverse=True)
        for game in games[: callback_data.limit]:
            item_id = game["item_id"]
            game_name = game["name"]
            first_cost = game["first_cost"]
            cost = game["cost"]
            time_in_game = game["time_in_game"]
            games_list.append((item_id, game_name, first_cost, time_in_game, cost))
    else:
        games_list = await get_games_from_db(
            steam_id=callback_data.steam_id,
            limit=callback_data.limit,
            order=callback_data.order,
            session=session,
        )
    return games_list


async def get_tracking_items_list_from_redis_or_db(session, telegram_id, storage):
    user_data = await redis_convert_to_dict(telegram_id=telegram_id, storage=storage)
    if user_data:
        tracking_items = user_data["tracking_items"]
        tracking_items_list = []
        for item_id, item_data in tracking_items.items():
            tracking_items_list.append(
                (
                    item_data["name"],
                    item_id,
                    item_data["first_cost"],
                    item_data["cost"],
                )
            )
    else:
        tracking_items_list = await get_all_tracking_items_from_db(
            telegram_id=telegram_id, session=session
        )
    return tracking_items_list


async def get_tracking_games_list_from_redis_or_db(session, telegram_id, storage):
    user_data = await redis_convert_to_dict(telegram_id=telegram_id, storage=storage)
    if user_data:
        tracking_items = user_data["tracking_games"]
        tracking_games_list = []
        for game_id, game_data in tracking_items.items():
            tracking_games_list.append(
                (
                    game_data["name"],
                    game_id,
                    game_data["first_cost"],
                    game_data["cost"],
                )
            )
    else:
        tracking_games_list = await get_all_tracking_games_from_db(
            telegram_id=telegram_id, session=session
        )
    return tracking_games_list


async def get_tracking_game_from_redis_or_db(
    telegram_id, callback_data, session, storage
):
    user_data = await redis_convert_to_dict(telegram_id=telegram_id, storage=storage)
    if user_data:
        game = user_data["tracking_games"][str(callback_data.game_id)]
    else:
        tracking_game_data = await get_tracking_game_data_from_db(
            game_id=callback_data.game_id, session=session
        )
        name, first_cost, cost = tracking_game_data[0]
        game = {"name": name, "first_cost": first_cost, "cost": cost}
    return game


async def get_tracking_item_from_redis_or_db(
    telegram_id, callback_data, session, storage
):
    user_data = await redis_convert_to_dict(telegram_id=telegram_id, storage=storage)
    if user_data:
        item = user_data["tracking_items"][str(callback_data.item_id)]
        name = item["name"]
    else:
        tracking_item_data = await get_tracking_item_data_from_db(
            item_id=callback_data.item_id, session=session
        )
        name, first_cost, cost = tracking_item_data[0]
        item = {"name": name, "first_cost": first_cost, "cost": cost}
        name = item["name"]
    return item, name


async def get_steam_ids_from_redis_or_db(session, storage, telegram_id):
    user_data = await redis_convert_to_dict(telegram_id=telegram_id, storage=storage)
    if user_data:
        steam_ids_list = user_data["steam_ids"]["ids"]
        steam_ids_list = [(steam_id, name) for steam_id, name in steam_ids_list.items()]
    else:
        steam_ids_list = await get_all_steam_ids_from_db(
            telegram_id=telegram_id, session=session
        )
    return steam_ids_list


async def check_game_exist_in_redis_or_db(telegram_id, game_id, session, storage):
    user_data = await redis_convert_to_dict(telegram_id=telegram_id, storage=storage)
    if user_data:
        tracking_games = user_data["tracking_games"]
        check_game = game_id in tracking_games
    else:
        check_game = await get_tracking_game_from_db(
            game_id=int(game_id), session=session
        )
    return check_game


async def check_item_exist_in_redis_or_db(telegram_id, item_id, session, storage):
    user_data = await redis_convert_to_dict(telegram_id=telegram_id, storage=storage)
    if user_data:
        tracking_items = user_data["tracking_items"]
        check_game = item_id in tracking_items
    else:
        check_game = await get_tracking_item_from_db(
            item_id=int(item_id), session=session
        )
    return check_game


async def check_steam_id_exist_in_redis_or_db(session, steam_id, storage, telegram_id):
    user_data = await redis_convert_to_dict(telegram_id=telegram_id, storage=storage)
    if user_data:
        steam_ids = user_data["steam_ids"]
        check_steam_id = str(steam_id) in steam_ids
    else:
        check_steam_id = await get_steamid_from_db(steam_id=steam_id, session=session)
    return check_steam_id
