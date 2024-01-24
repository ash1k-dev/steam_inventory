from unittest import mock

import pytest

from core.steam.steam import get_steam_id, get_steam_name
from core.tests.test_steam.test_steam_ids.steam_ids_test_data import (
    LIST_STEAM_ID,
    LIST_STEAM_NAME,
)


@pytest.mark.parametrize(
    "test_data_steam_id, test_result_steam_id",
    LIST_STEAM_ID,
)
def test_get_steam_id(
    test_data_steam_id: dict,
    test_result_steam_id: int,
    get_steam_id_requests_mock: mock.Mock,
) -> None:
    get_steam_id_requests_mock.return_value.json.return_value = test_data_steam_id
    result = get_steam_id(steam_id="")
    assert result == test_result_steam_id


@pytest.mark.parametrize(
    "test_data_steam_name, test_result_steam_name",
    LIST_STEAM_NAME,
)
def test_steam_name(
    test_data_steam_name: dict,
    test_result_steam_name: str,
    get_steam_id_requests_mock: mock.Mock,
) -> None:
    get_steam_id_requests_mock.return_value.json.return_value = test_data_steam_name
    result = get_steam_name(steam_id=1)
    assert result == test_result_steam_name
