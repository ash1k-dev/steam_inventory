import pytest

from core.steam.steam import get_all_games_info, get_game_cost, get_game_name
from core.tests.test_steam.test_games.games_test_data import (
    LIST_ALL_GAMES_INFO,
    LIST_GAME_COST,
    LIST_GAME_NAME,
)


@pytest.mark.parametrize(
    "test_data, test_result, test_game_id",
    LIST_GAME_COST,
)
def test_get_game_cost(test_data, test_result, test_game_id, get_game_requests_mock):
    get_game_requests_mock.return_value.json.return_value = test_data
    result = get_game_cost(game_id=test_game_id)
    assert result == test_result


@pytest.mark.parametrize(
    "test_data, test_result, test_game_id",
    LIST_GAME_NAME,
)
def test_get_game_name(test_data, test_result, test_game_id, get_game_requests_mock):
    get_game_requests_mock.return_value.json.return_value = test_data
    result = get_game_name(game_id=test_game_id)
    assert result == test_result


@pytest.mark.parametrize(
    "test_data, test_result",
    LIST_ALL_GAMES_INFO,
)
def test_get_all_games_info(
    test_data, test_result, get_game_requests_mock, get_game_cost_mock
):
    get_game_requests_mock.return_value.json.return_value = test_data
    result = get_all_games_info(steam_id=1)
    assert result == test_result
