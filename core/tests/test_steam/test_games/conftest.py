from typing import Any, Callable
from unittest import mock

import pytest

from core.tests.test_steam.test_games.games_test_data import GAME_COST_DICT


@pytest.fixture
def get_game_requests_mock(monkeypatch) -> mock.Mock:
    """Замена функции get_game_requests"""
    game_requests_mock = mock.Mock()
    monkeypatch.setattr("core.steam.steam.requests.get", game_requests_mock)
    return game_requests_mock


def game_cost_mock(game_id) -> float:
    """Получение стоимости игры из словаря"""
    game_cost_dict = GAME_COST_DICT
    return game_cost_dict.get(game_id)


@pytest.fixture
def get_game_cost_mock(monkeypatch) -> Callable[[Any], float]:
    """Замена функции get_game_cost"""
    monkeypatch.setattr("core.steam.steam.get_game_cost", game_cost_mock)
    return game_cost_mock
