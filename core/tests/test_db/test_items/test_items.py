from typing import Any, Callable

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from config import DEPRECIATION_FACTOR, INCREASE_FACTOR
from core.db.methods.create import (
    create_all_items,
    create_all_steam_inventories,
    create_item,
    create_item_track,
    create_steam,
    create_user,
)
from core.db.methods.delete import delete_tracking_item
from core.db.methods.request import (
    get_all_items_from_db,
    get_all_tracking_items_from_db,
    get_amount_and_items_info_from_db,
    get_inventories_id_from_db,
    get_item_from_db,
    get_items_changes,
    get_items_classid_list_from_db,
    get_items_info_from_db,
    get_steamid_from_db,
    get_tracking_item_data_from_db,
    get_tracking_item_from_db,
    get_tracking_items_changes,
)
from core.steam.steam import get_all_items_info
from core.tests.test_db.test_items.items_test_data import (
    LIST_ITEMS_CRUD,
    LIST_TRACKING_ITEMS_CRUD,
)


async def update_current_item_cost(item_id: int, item_type: str, session: AsyncSession):
    """Обновление текущую стоимость предмета"""
    factor = {"item": INCREASE_FACTOR, "tracking_item": DEPRECIATION_FACTOR}
    item_from_db = await get_item_from_db(item_id=item_id, session=session)
    item_from_db.cost = item_from_db.cost * factor.get(item_type)
    session.add(item_from_db)
    await session.commit()


@pytest.mark.parametrize(
    "test_data_user,"
    "test_data_all_games,"
    "test_data_json,"
    "test_data_item_add,"
    "test_data_amount_and_items,"
    "test_data_classid,"
    "test_result_items_info,"
    "test_result_all_items_len,"
    "test_result_item_change",
    LIST_ITEMS_CRUD,
)
@pytest.mark.asyncio
async def test_items_crud(
    test_data_user: dict,
    test_data_all_games: dict,
    test_data_json: dict,
    test_data_item_add: dict,
    test_data_amount_and_items: dict,
    test_data_classid: list,
    test_result_items_info: dict,
    test_result_all_items_len: dict,
    test_result_item_change: list,
    get_item_cost_from_steam_mock: Callable[[Any], float],
    get_item_sleep_mock: Callable[[Any], None],
    session: AsyncSession,
) -> None:
    """Тестирование CRUD для предметов"""
    get_item_sleep_mock.return_value = None
    await create_user(
        name=test_data_user["name"],
        telegram_id=test_data_user["telegram_id"],
        session=session,
    )
    await create_steam(
        steam_id=test_data_user["steam_id"],
        telegram_id=test_data_user["telegram_id"],
        steam_name=test_data_user["steam_name"],
        session=session,
    )
    steam = await get_steamid_from_db(
        steam_id=test_data_user["steam_id"], session=session
    )
    await create_all_steam_inventories(
        all_games_info=test_data_all_games, steam_id=steam.id, session=session
    )
    for game_id in test_data_all_games:
        inventory_id = await get_inventories_id_from_db(
            session=session, steam_id=steam.id, games_id=game_id
        )
        all_items_info = get_all_items_info(test_data_json)
        await create_all_items(
            all_items_info, inventory_id=inventory_id.id, session=session
        )

    amount_and_items_info = await get_amount_and_items_info_from_db(
        session=session,
        steam_id=test_data_user["steam_id"],
        limit=1000,
        order="cost",
        games_id=730,
    )
    assert amount_and_items_info == test_data_amount_and_items
    items_classid_list = await get_items_classid_list_from_db(session=session)
    assert items_classid_list == test_data_classid
    items_info = await get_items_info_from_db(
        session=session, steam_id=test_data_user["steam_id"]
    )
    assert items_info == test_result_items_info
    all_items = await get_all_items_from_db(session=session)
    assert len(all_items) == test_result_all_items_len["len"]
    await create_item(
        name=test_data_item_add["name"],
        item_id=test_data_item_add["item_id"],
        item_cost=test_data_item_add["item_cost"],
        session=session,
    )
    all_items_after_add = await get_all_items_from_db(session=session)
    assert len(all_items_after_add) == test_result_all_items_len["len_after_add"]
    for item in all_items_after_add:
        item_from_db = await get_item_from_db(item_id=item.classid, session=session)
        assert item_from_db is not None
        assert item_from_db.name == item.name
        assert item_from_db.app_id == item.app_id
        assert item_from_db.classid == item.classid
        assert item_from_db.cost == item.cost
        await update_current_item_cost(
            item_id=item_from_db.classid,
            item_type="item",
            session=session,
        )

    items_changes = await get_items_changes(
        session, telegram_id=test_data_user["telegram_id"]
    )
    assert items_changes == test_result_item_change


@pytest.mark.parametrize(
    "test_data_user,"
    "test_data_all_tracking_items,"
    "test_result_tracking_items_change,"
    "test_result_all_tracking_items_len",
    LIST_TRACKING_ITEMS_CRUD,
)
@pytest.mark.asyncio
async def test_tracking_items_crud(
    test_data_user: dict,
    test_data_all_tracking_items: dict,
    test_result_tracking_items_change: list,
    test_result_all_tracking_items_len: int,
    get_item_cost_from_create_mock: Callable[[Any], float],
    get_item_name_mock: Callable[[Any], str],
    session: AsyncSession,
) -> None:
    """Тестирование CRUD для отслеживаемых предметов"""
    await create_user(
        name=test_data_user["name"],
        telegram_id=test_data_user["telegram_id"],
        session=session,
    )
    for item_id, item_data in test_data_all_tracking_items.items():
        await create_item_track(
            item_id=item_id, telegram_id=test_data_user["telegram_id"], session=session
        )
        tracking_item = await get_tracking_item_from_db(
            item_id=item_id, session=session
        )
        assert tracking_item is not None
        assert tracking_item.name == item_data["name"]
        assert tracking_item.item_id == item_id
        assert tracking_item.first_cost == item_data["cost"]
        await get_tracking_item_data_from_db(item_id=item_id, session=session)

    all_tracking_items = await get_all_tracking_items_from_db(
        telegram_id=test_data_user["telegram_id"], session=session
    )
    assert len(all_tracking_items) == test_result_all_tracking_items_len

    for item_id in test_data_all_tracking_items:
        await update_current_item_cost(
            item_id=item_id, item_type="tracking_item", session=session
        )

    tracking_items_changes = await get_tracking_items_changes(
        session=session, telegram_id=test_data_user["telegram_id"]
    )
    assert tracking_items_changes == test_result_tracking_items_change

    for item_id in test_data_all_tracking_items:
        await delete_tracking_item(item_id=item_id, session=session)
        tracking_item = await get_tracking_item_from_db(
            item_id=item_id, session=session
        )
        assert tracking_item is None
