from typing import Any, Callable
from unittest import mock

import pytest

from core.steam.steam import get_all_games_info, get_game_cost, get_game_name
from core.tests.test_steam.test_games.games_test_data import (
    LIST_ALL_GAMES_INFO,
    LIST_GAME_COST,
    LIST_GAME_NAME,
)


@pytest.mark.parametrize(
    "test_data_game_cost, test_result_game_cost, test_data_game_id",
    LIST_GAME_COST,
)
def test_get_game_cost(
    test_data_game_cost: dict,
    test_result_game_cost: float,
    test_data_game_id: int,
    get_game_requests_mock: mock.Mock,
) -> None:
    """Проверка функции получения стоимости игры"""
    get_game_requests_mock.return_value.json.return_value = test_data_game_cost
    result = get_game_cost(game_id=test_data_game_id)
    assert result == test_result_game_cost


@pytest.mark.parametrize(
    "test_data_game_name, test_result_game_name, test_data_game_id",
    LIST_GAME_NAME,
)
def test_get_game_name(
    test_data_game_name: dict,
    test_result_game_name: str,
    test_data_game_id: int,
    get_game_requests_mock: mock.Mock,
) -> None:
    """Проверка функции получения названия игры"""
    get_game_requests_mock.return_value.json.return_value = test_data_game_name
    result = get_game_name(game_id=test_data_game_id)
    assert result == test_result_game_name


@pytest.mark.parametrize(
    "test_data_all_games, test_result_all_games",
    LIST_ALL_GAMES_INFO,
)
def test_get_all_games_info(
    test_data_all_games: dict,
    test_result_all_games: dict,
    get_game_requests_mock: mock.Mock,
    get_game_cost_mock: Callable[[Any], float],
) -> None:
    """Проверка функции получения информации о всех играх"""
    get_game_requests_mock.return_value.json.return_value = test_data_all_games
    result = get_all_games_info(steam_id=1)
    assert result == test_result_all_games
