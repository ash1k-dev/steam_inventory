from sqlalchemy.ext.asyncio import AsyncSession

from core.db.methods.request import get_steamid_from_db, get_tracking_game_from_db


async def delete_steam_id(steam_id: str, session: AsyncSession) -> None:
    """Deleting steam id"""
    steam_id = await get_steamid_from_db(steam_id=int(steam_id), session=session)
    await session.delete(steam_id)
    await session.commit()


async def delete_tracking_game(game_id: int, session: AsyncSession) -> None:
    """Deleting steam id"""
    tracking_game = await get_tracking_game_from_db(game_id=game_id, session=session)
    await session.delete(tracking_game)
    await session.commit()
