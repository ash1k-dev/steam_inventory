import asyncio
from typing import Any, Callable

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DB_URL_TEST
from core.db.models import models
from core.tests.test_db.test_games.games_test_data import (
    TEST_DATA_TRACKING_GAMES_COST_BEFORE_DECREASE,
    TEST_DATA_TRACKING_GAMES_NAME,
)

engine = create_async_engine(DB_URL_TEST, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop(request) -> asyncio.AbstractEventLoop:
    """"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def db() -> None:
    """Создание и последующие очистка таблиц в базе данных"""
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def session() -> AsyncSession:
    """Создание сессии"""
    async with async_session() as session:
        yield session


def game_cost_mock(game_id) -> float:
    """Получение стоимости игры из словаря"""
    game_cost_dict = TEST_DATA_TRACKING_GAMES_COST_BEFORE_DECREASE
    return game_cost_dict.get(game_id)


@pytest.fixture
def get_game_cost_mock(monkeypatch) -> Callable[[Any], float]:
    """Замена функции get_game_cost"""
    monkeypatch.setattr("core.db.methods.create.get_game_cost", game_cost_mock)
    return game_cost_mock


def game_name_mock(game_id: int) -> str:
    """Получение названия игры из словаря"""
    game_cost_dict = TEST_DATA_TRACKING_GAMES_NAME
    return game_cost_dict.get(game_id)


@pytest.fixture
def get_game_name_mock(monkeypatch) -> Callable[[Any], str]:
    """Замена функции get_game_name"""
    monkeypatch.setattr("core.db.methods.create.get_game_name", game_name_mock)
    return game_name_mock
