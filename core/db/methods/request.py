from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.models import (
    User,
    SteamId,
    Game,
    GameInAccount,
    SteamInventory,
    SteamItem,
    SteamItemsInInventory,
    # ItemTrack,
    GameTrack,
)


async def get_user_from_db(telegram_id: int, session: AsyncSession):
    """Getting a user from the database"""
    statement = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


"Нужно добавить провекру по user id, steam_id может дублироваться"


async def get_steamid_from_db(steam_id: int, session: AsyncSession):
    statement = select(SteamId).where(SteamId.steam_id == steam_id)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_all_steam_ids_from_db(telegram_id: int, session: AsyncSession):
    """Getting all steam ids from the database"""
    user = await get_user_from_db(telegram_id=telegram_id, session=session)
    statement = select(SteamId).where(SteamId.user_id == user.id)
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
        order = Game.game_cost
    elif order == "all":
        order = GameInAccount.time_in_game
    steam_id = await get_steamid_from_db(steam_id=steam_id, session=session)
    statement = (
        select(
            GameInAccount.game_id,
            GameInAccount.game_name,
            GameInAccount.first_game_cost,
            GameInAccount.time_in_game,
            Game.game_cost,
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
            func.sum(Game.game_cost),
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
    statement = select(SteamInventory).filter(
        SteamInventory.steam_id == steam_id, SteamInventory.games_id == 730
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
            func.sum(SteamItem.item_cost),
            func.sum(SteamItemsInInventory.first_item_cost),
            func.sum(SteamItemsInInventory.amount),
            func.max(SteamItem.item_cost),
            func.min(SteamItem.item_cost),
        )
        .join(SteamItem, SteamItem.classid == SteamItemsInInventory.item_id)
        .where(SteamInventory.id == inventory_id.id)
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
            SteamItem.name,
            SteamItem.item_cost,
            SteamItemsInInventory.first_item_cost,
            SteamItemsInInventory.amount,
        )
        .join(SteamItem, SteamItem.classid == SteamItemsInInventory.item_id)
        .where(SteamInventory.id == inventory_id.id)
    )
    result = await session.execute(statement)
    return result.all()


async def get_items_list_from_db(
    session: AsyncSession,
):
    statement = select(SteamItem.classid)
    result = await session.execute(statement)
    return result.scalars().all()


async def get_games_list_from_db(
    session: AsyncSession,
):
    statement = select(Game.game_id)
    result = await session.execute(statement)
    return result.scalars().all()


# async def get_all_tracking_items_from_db(telegram_id: int, session: AsyncSession):
#     """Getting all steam ids from the database"""
#     user = await get_user_from_db(telegram_id=telegram_id, session=session)
#     statement = select(ItemTrack).where(ItemTrack.user_id == user.id)
#     result = await session.execute(statement)
#     return result.scalars().all()


async def get_all_tracking_games_from_db(telegram_id: int, session: AsyncSession):
    """Getting all steam ids from the database"""
    # user = await get_user_from_db(telegram_id=telegram_id, session=session)
    # statement = select(GameTrack).where(GameTrack.user_id == user.id)
    # result = await session.execute(statement)
    # return result.scalars().all()
    user = await get_user_from_db(telegram_id=telegram_id, session=session)
    statement = (
        select(
            GameTrack.user_id,
            GameTrack.name,
            GameTrack.game_id,
            GameTrack.first_game_cost,
            Game.game_cost,
        )
        .join(Game, Game.game_id == GameTrack.game_id)
        .where(GameTrack.user_id == user.id)
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
