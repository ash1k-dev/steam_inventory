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
    "test_data, test_result",
    LIST_STEAM_INVENTORY,
)
def test_get_steam_inventory(test_data, test_result, get_items_requests_mock):
    get_items_requests_mock.return_value.json.return_value = test_data
    result = get_steam_inventory(steam_id=1, game_id=730)
    assert result == test_result


@pytest.mark.parametrize(
    "test_data, test_result, item_name",
    LIST_ITEM_COST,
)
def test_get_item_cost(test_data, test_result, item_name, get_items_requests_mock):
    get_items_requests_mock.return_value.json.return_value = test_data
    result = get_item_cost(name=item_name, game_id=730, currency=5)
    assert result == test_result


@pytest.mark.parametrize(
    "test_data, test_result, item_id",
    LIST_ITEM_MARKET_HASH_NAME,
)
def test_get_item_market_hash_name(
    test_data, test_result, item_id, get_items_requests_mock
):
    get_items_requests_mock.return_value.json.return_value = test_data
    result = get_item_market_hash_name(item_id=item_id, app_id=730)
    assert result == test_result


@pytest.mark.parametrize("test_data, test_result", LIST_INITIAL_ITEMS)
def test_get_all_items_info(
    test_data, test_result, get_item_cost_mock, get_item_sleep_mock
):
    get_item_sleep_mock.return_value = None
    result = get_all_items_info(test_data)
    assert result == test_result