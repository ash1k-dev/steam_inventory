from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.models import User, SteamId


async def get_user_from_db(telegram_id: int, session: AsyncSession):
    """Getting a user from the database"""
    statement = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_steamid_from_db(steam_id, session: AsyncSession):
    statement = select(SteamId).where(SteamId.steam_id == steam_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def check_steam_id_in_db(steam_id, session):
    statement = select(SteamId).where(SteamId.steam_id == steam_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_all_steam_ids_from_db(telegram_id: int, session: AsyncSession):
    """Getting all steam ids from the database"""
    user = await get_user_from_db(telegram_id=telegram_id, session=session)
    statement = select(SteamId).where(SteamId.user_id == user.id)
    result = await session.execute(statement)
    return result.scalars().all()
