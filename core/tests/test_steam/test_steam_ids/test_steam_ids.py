import pytest

from core.steam.steam import get_steam_id, get_steam_name
from core.tests.test_steam.test_steam_ids.steam_ids_test_data import (
    LIST_STEAM_ID,
    LIST_STEAM_NAME,
)


@pytest.mark.parametrize(
    "test_data, test_result",
    LIST_STEAM_ID,
)
def test_get_steam_id(test_data, test_result, get_steam_id_requests_mock):
    get_steam_id_requests_mock.return_value.json.return_value = test_data
    result = get_steam_id(steam_id="")
    assert result == test_result


@pytest.mark.parametrize(
    "test_data, test_result",
    LIST_STEAM_NAME,
)
def test_steam_name(test_data, test_result, get_steam_id_requests_mock):
    get_steam_id_requests_mock.return_value.json.return_value = test_data
    result = get_steam_name(steam_id=1)
    assert result == test_result
