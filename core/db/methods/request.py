from sqlalchemy import select, desc, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.models import (
    User,
    SteamId,
    Game,
    SteamInventory,
    SteamItem,
    SteamItemsInInventory,
)


async def get_user_from_db(telegram_id: int, session: AsyncSession):
    """Getting a user from the database"""
    statement = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_steamid_from_db(steam_id: int, session: AsyncSession):
    statement = select(SteamId).where(SteamId.steam_id == steam_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def check_steam_id_in_db(steam_id: int, session):
    statement = select(SteamId).where(SteamId.steam_id == steam_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_all_steam_ids_from_db(telegram_id: int, session: AsyncSession):
    """Getting all steam ids from the database"""
    user = await get_user_from_db(telegram_id=telegram_id, session=session)
    statement = select(SteamId).where(SteamId.user_id == user.id)
    # statement = select(SteamId).filter(User.telegram_id == telegram_id)
    result = await session.execute(statement)
    return result.scalars().all()


# async def get_all_games_from_db(telegram_id: int, session: AsyncSession):
#     """Getting all steam ids from the database"""
#     user = await get_user_from_db(telegram_id=telegram_id, session=session)
#     statement = select(Game).where(SteamId.user_id == user.id)
#     result = await session.execute(statement)
#     return result.scalars().all()


async def get_top_games_from_db(
    telegram_id: int,
    limit: int,
    order: str,
    session: AsyncSession,
):
    """Getting games from the database"""
    if order == "time":
        order = Game.time_in_game
    elif order == "cost":
        order = Game.game_cost
    user = await get_user_from_db(telegram_id=telegram_id, session=session)
    statement = (
        select(Game)
        .where(SteamId.user_id == user.id)
        .limit(limit)
        .order_by(desc(order))
    )
    result = await session.execute(statement)
    return result.scalars().all()


async def get_games_info_from_db(
    session: AsyncSession,
    steam_id: int,
):
    steamid = await get_steamid_from_db(steam_id, session=session)
    statement = select(
        (func.count(Game.time_in_game)),
        (func.sum(Game.game_cost)),
        (func.sum(Game.time_in_game)),
    ).where(Game.steam_id == steamid.id)
    result = await session.execute(statement)
    return result.all()


async def get_inventorys_id_from_db(steam_id, session: AsyncSession):
    statement = select(SteamInventory).filter(
        SteamInventory.steam_id == steam_id, SteamInventory.games_id == 730
    )
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_amount_and_items_info_from_db(
    session: AsyncSession,
    steam_id,
):
    steamid_from_db = await get_steamid_from_db(steam_id=steam_id, session=session)
    inventory_id = await get_inventorys_id_from_db(
        session=session, steam_id=steamid_from_db.id
    )
    statement = (
        select(SteamItemsInInventory)
        .options(joinedload(SteamItemsInInventory.steam_item))
        .where(SteamInventory.id == inventory_id.id)
        .order_by(desc(SteamItemsInInventory.amount))
    )
    result = await session.execute(statement)
    return result.scalars().all()
