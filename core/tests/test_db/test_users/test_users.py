import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.methods.create import (
    create_all_steam_inventories,
    create_steam,
    create_user,
)
from core.db.methods.delete import delete_steam_id
from core.db.methods.request import (
    get_all_inventory_ids_from_db,
    get_all_steam_ids_from_db,
    get_all_user_from_db,
    get_inventories_id_from_db,
    get_steamid_from_db,
    get_user_from_db,
)
from core.tests.test_db.test_users.users_test_data import (
    LIST_INVENTORY_CRUD,
    LIST_STEAM_ID_CRUD,
    LIST_USER_CRUD,
)


@pytest.mark.parametrize(
    "test_data_user," "test_result_users_len," "test_data_user_not_exist",
    LIST_USER_CRUD,
)
@pytest.mark.asyncio
async def test_user_crud(
    test_data_user: list,
    test_result_users_len: int,
    test_data_user_not_exist: int,
    session: AsyncSession,
) -> None:
    """Тестирование CRUD для пользователей"""
    for user in test_data_user:
        await create_user(
            name=user["name"], telegram_id=user["telegram_id"], session=session
        )
    user = await get_user_from_db(
        telegram_id=test_data_user[0]["telegram_id"], session=session
    )
    assert user.name == test_data_user[0]["name"]
    assert user.telegram_id == test_data_user[0]["telegram_id"]
    user_not_exist = await get_user_from_db(
        telegram_id=test_data_user_not_exist, session=session
    )
    assert user_not_exist is None
    users = await get_all_user_from_db(session=session)
    assert len(users) == test_result_users_len


@pytest.mark.parametrize(
    "test_data_steam_id,"
    "test_result_len_before,"
    "test_result_len_after,"
    "test_data_steam_id_not_exist",
    LIST_STEAM_ID_CRUD,
)
@pytest.mark.asyncio
async def test_steam_id_crud(
    test_data_steam_id: list,
    test_result_len_before: int,
    test_result_len_after: int,
    test_data_steam_id_not_exist: int,
    session: AsyncSession,
) -> None:
    """Тестирование CRUD для Steam id"""
    await create_user(
        name=test_data_steam_id[0]["steam_name"],
        telegram_id=test_data_steam_id[0]["telegram_id"],
        session=session,
    )
    for steam in test_data_steam_id:
        await create_steam(
            steam_id=steam["steam_id"],
            telegram_id=steam["telegram_id"],
            steam_name=steam["steam_name"],
            session=session,
        )
    steam = await get_steamid_from_db(
        steam_id=test_data_steam_id[0]["steam_id"], session=session
    )
    assert steam.steam_id == test_data_steam_id[0]["steam_id"]
    assert steam.user_id == test_data_steam_id[0]["telegram_id"]
    assert steam.name == test_data_steam_id[0]["steam_name"]
    steam_not_exist = await get_steamid_from_db(
        steam_id=test_data_steam_id_not_exist, session=session
    )
    assert steam_not_exist is None
    steam_ids_before = await get_all_steam_ids_from_db(
        telegram_id=test_data_steam_id[0]["telegram_id"], session=session
    )
    assert len(steam_ids_before) == test_result_len_before
    await delete_steam_id(steam_id=test_data_steam_id[0]["steam_id"], session=session)
    steam_ids_after = await get_all_steam_ids_from_db(
        telegram_id=test_data_steam_id[0]["telegram_id"], session=session
    )
    assert len(steam_ids_after) == test_result_len_after


@pytest.mark.parametrize(
    "test_data_inventory,"
    "test_data_games,"
    "test_result_len_before,"
    "test_result_len_after,"
    "test_data_inventory_not_exist",
    LIST_INVENTORY_CRUD,
)
@pytest.mark.asyncio
async def test_inventory_crud(
    test_data_inventory: dict,
    test_data_games: dict,
    test_result_len_before: int,
    test_result_len_after: int,
    test_data_inventory_not_exist: int,
    session: AsyncSession,
):
    """Тестирование CRUD для инвентарей"""
    await create_user(
        name=test_data_inventory["name"],
        telegram_id=test_data_inventory["telegram_id"],
        session=session,
    )
    await create_steam(
        steam_id=test_data_inventory["steam_id"],
        telegram_id=test_data_inventory["telegram_id"],
        steam_name=test_data_inventory["steam_name"],
        session=session,
    )
    steam = await get_steamid_from_db(
        steam_id=test_data_inventory["steam_id"], session=session
    )
    await create_all_steam_inventories(
        all_games_info=test_data_games, steam_id=steam.id, session=session
    )
    all_inventory = await get_all_inventory_ids_from_db(
        steam_id=steam.id, session=session
    )
    assert len(all_inventory) == test_result_len_before
    for game_id in test_data_games:
        inventory = await get_inventories_id_from_db(
            steam_id=steam.id, games_id=game_id, session=session
        )
        assert inventory.games_id == game_id
        assert inventory.steam_id == steam.id
    inventory_not_exist = await get_inventories_id_from_db(
        steam_id=steam.id,
        games_id=test_data_inventory_not_exist,
        session=session,
    )
    assert inventory_not_exist is None
    await delete_steam_id(steam_id=test_data_inventory["steam_id"], session=session)
    all_inventory_after = await get_all_inventory_ids_from_db(
        steam_id=steam.id, session=session
    )
    assert len(all_inventory_after) == test_result_len_after
