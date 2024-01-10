from unittest import mock

import pytest

from core.tests.test_steam.test_games.games_test_data import GAME_COST_DICT


@pytest.fixture
def get_game_requests_mock(monkeypatch):
    game_requests_mock = mock.Mock()
    monkeypatch.setattr("core.steam.steam.requests.get", game_requests_mock)
    return game_requests_mock


@pytest.fixture
def get_games_info_without_cost_mock(monkeypatch):
    games_info_without_cost_mock = mock.Mock()
    monkeypatch.setattr(
        "core.steam.steam.get_games_info_without_cost", games_info_without_cost_mock
    )
    return games_info_without_cost_mock


def game_cost_mock(game_id):
    game_cost_dict = GAME_COST_DICT
    return game_cost_dict.get(game_id)


@pytest.fixture
def get_game_cost_mock(monkeypatch):
    monkeypatch.setattr("core.steam.steam.get_game_cost", game_cost_mock)
    return game_cost_mock
