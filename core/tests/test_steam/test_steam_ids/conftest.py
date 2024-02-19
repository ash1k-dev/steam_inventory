from unittest import mock

import pytest


@pytest.fixture
def get_steam_id_requests_mock(monkeypatch) -> mock.Mock:
    """Замена функции requests.get"""
    steam_id_requests_mock = mock.Mock()
    monkeypatch.setattr("core.steam.steam.requests.get", steam_id_requests_mock)
    return steam_id_requests_mock
