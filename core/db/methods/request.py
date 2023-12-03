from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.models import (
    User,
    Steam,
    Game,
    GameInAccount,
    Inventory,
    Item,
    ItemInInventory,
    # ItemTrack,
    GameTrack,
    ItemTrack,
)


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
    statement = select(Steam).where(Steam.user_id == telegram_id)
    result = await session.execute(statement)
    return result.scalars().all()


#
async def get_top_games_from_db(
    steam_id: int,
    limit: int,
    order: str,
    session: AsyncSession,
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
        .where(Inventory.id == inventory_id.id)
    )
    result = await session.execute(statement)
    return result.all()


async def get_amount_and_items_info_from_db(
    session: AsyncSession,
    steam_id,
):
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
        )
        .join(Item, Item.classid == ItemInInventory.item_id)
        .where(Inventory.id == inventory_id.id)
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
            ItemTrack.first_cost,
            ItemTrack.user_id,
            ItemTrack.item_id,
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
            GameTrack.user_id,
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
