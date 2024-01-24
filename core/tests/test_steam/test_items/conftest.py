from typing import Any, Callable
from unittest import mock

import pytest

from core.tests.test_steam.test_items.items_test_data import ITEM_COST_DICT


@pytest.fixture
def get_items_requests_mock(monkeypatch) -> mock.Mock:
    items_requests_mock = mock.Mock()
    monkeypatch.setattr("core.steam.steam.requests.get", items_requests_mock)
    return items_requests_mock


def item_cost_mock(item_name) -> float:
    item_cost_dict = ITEM_COST_DICT
    return item_cost_dict.get(item_name)


@pytest.fixture
def get_item_cost_mock(monkeypatch) -> Callable[[Any], float]:
    monkeypatch.setattr("core.steam.steam.get_item_cost", item_cost_mock)
    return item_cost_mock


@pytest.fixture
def get_item_sleep_mock(monkeypatch) -> mock.Mock:
    sleep_mock = mock.Mock()
    monkeypatch.setattr("core.steam.steam.sleep", sleep_mock)
    return sleep_mock
