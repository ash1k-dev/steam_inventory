from unittest import mock

import pytest

from core.steam.steam import (
    get_all_items_info,
    get_item_cost,
    get_item_market_hash_name,
    get_steam_inventory,
)
from core.tests.test_steam.test_items.items_test_data import (
    LIST_INITIAL_ITEMS,
    LIST_ITEM_COST,
    LIST_ITEM_MARKET_HASH_NAME,
    LIST_STEAM_INVENTORY,
)


@pytest.mark.parametrize(
    "test_data_inventory, test_result_inventory",
    LIST_STEAM_INVENTORY,
)
def test_get_steam_inventory(
    test_data_inventory: dict,
    test_result_inventory: dict,
    get_items_requests_mock: mock.Mock,
) -> None:
    """Проверка получения инвентаря Steam"""
    get_items_requests_mock.return_value.json.return_value = test_data_inventory
    result = get_steam_inventory(steam_id=1, game_id=730)
    assert result == test_result_inventory


@pytest.mark.parametrize(
    "test_data_item_cost, test_result_item_cost, test_data_item_name",
    LIST_ITEM_COST,
)
def test_get_item_cost(
    test_data_item_cost: dict,
    test_result_item_cost: float,
    test_data_item_name: str,
    get_items_requests_mock: mock.Mock,
) -> None:
    """Проверка получения стоимости предмета"""
    get_items_requests_mock.return_value.json.return_value = test_data_item_cost
    result = get_item_cost(name=test_data_item_name, game_id=730, currency=5)
    assert result == test_result_item_cost


@pytest.mark.parametrize(
    "test_data_item_name, test_result_item_name, test_data_item_id",
    LIST_ITEM_MARKET_HASH_NAME,
)
def test_get_item_market_hash_name(
    test_data_item_name: dict,
    test_result_item_name: str,
    test_data_item_id: int,
    get_items_requests_mock: mock.Mock,
) -> None:
    """Проверка получения названия предмета"""
    get_items_requests_mock.return_value.json.return_value = test_data_item_name
    result = get_item_market_hash_name(item_id=test_data_item_id, app_id=730)
    assert result == test_result_item_name


@pytest.mark.parametrize(
    "test_data_all_items, test_result_all_items", LIST_INITIAL_ITEMS
)
def test_get_all_items_info(
    test_data_all_items: dict,
    test_result_all_items: dict,
    get_item_cost_mock: mock.Mock,
    get_item_sleep_mock: mock.Mock,
) -> None:
    """Проверка получения информации о предметах"""
    get_item_sleep_mock.return_value = None
    result = get_all_items_info(test_data_all_items)
    assert result == test_result_all_items
