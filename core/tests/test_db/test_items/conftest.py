import asyncio
from typing import Any, Callable
from unittest import mock

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DB_URL_TEST
from core.db.models import models
from core.tests.test_db.test_items.items_test_data import (
    TEST_DATA_ITEM_COST_DICT,
    TEST_DATA_ITEM_NAME_DICT,
)

engine = create_async_engine(DB_URL_TEST, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop(request) -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def session() -> AsyncSession:
    async with async_session() as session:
        yield session


def item_cost_mock(name) -> float:
    item_cost_dict = TEST_DATA_ITEM_COST_DICT
    return item_cost_dict.get(name)


@pytest.fixture
def get_item_cost_from_create_mock(monkeypatch) -> Callable[[Any], float]:
    monkeypatch.setattr("core.db.methods.create.get_item_cost", item_cost_mock)
    return item_cost_mock


@pytest.fixture
def get_item_cost_from_steam_mock(monkeypatch) -> Callable[[Any], float]:
    monkeypatch.setattr("core.steam.steam.get_item_cost", item_cost_mock)
    return item_cost_mock


def item_name_mock(item_id) -> str:
    item_cost_dict = TEST_DATA_ITEM_NAME_DICT
    return item_cost_dict.get(item_id)


@pytest.fixture
def get_item_name_mock(monkeypatch) -> Callable[[Any], str]:
    monkeypatch.setattr(
        "core.db.methods.create.get_item_market_hash_name", item_name_mock
    )
    return item_name_mock


@pytest.fixture
def get_item_sleep_mock(monkeypatch) -> Callable[[Any], float]:
    sleep_mock = mock.Mock()
    monkeypatch.setattr("core.steam.steam.sleep", sleep_mock)
    return sleep_mock
