from typing import Any, Callable

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from config import DEPRECIATION_FACTOR
from core.db.methods.create import (
    create_all_games,
    create_game,
    create_game_track,
    create_steam,
    create_user,
)
from core.db.methods.delete import delete_tracking_game
from core.db.methods.request import (
    get_all_games_from_db,
    get_all_tracking_games_from_db,
    get_game_from_db,
    get_games_from_db,
    get_games_info_from_db,
    get_steamid_from_db,
    get_tracking_game_data_from_db,
    get_tracking_game_from_db,
    get_tracking_games_changes,
)
from core.tests.test_db.test_games.games_test_data import (
    LIST_GAMES_CRUD,
    LIST_TRACKING_GAMES_CRUD,
)


async def update_current_game_cost(game_id: int, session: AsyncSession) -> None:
    game_from_db = await get_game_from_db(game_id=game_id, session=session)
    game_from_db.cost = game_from_db.cost * DEPRECIATION_FACTOR
    session.add(game_from_db)
    await session.commit()


@pytest.mark.parametrize(
    "test_data_user,"
    "test_data_all_games,"
    "test_result_games,"
    "test_result_games_info,"
    "test_result_games_count,"
    "test_data_games_add",
    LIST_GAMES_CRUD,
)
@pytest.mark.asyncio
async def test_game_crud(
    test_data_user: dict,
    test_data_all_games: dict,
    test_result_games: list,
    test_result_games_info: list,
    test_result_games_count: int,
    test_data_games_add: dict,
    session: AsyncSession,
) -> None:
    await create_user(
        name=test_data_user["name"],
        telegram_id=test_data_user["telegram_id"],
        session=session,
    )
    await create_steam(
        steam_id=test_data_user["steam_id"],
        telegram_id=test_data_user["telegram_id"],
        steam_name=test_data_user["steam_name"],
        session=session,
    )
    steam = await get_steamid_from_db(
        steam_id=test_data_user["steam_id"], session=session
    )
    await create_all_games(
        all_games_info=test_data_all_games, steam_id=steam.id, session=session
    )
    games = await get_games_from_db(
        steam_id=test_data_user["steam_id"], session=session, limit=1000, order="cost"
    )
    assert games == test_result_games
    games_info = await get_games_info_from_db(
        steam_id=test_data_user["steam_id"], session=session
    )
    assert games_info == test_result_games_info
    all_games = await get_all_games_from_db(session=session)
    assert len(all_games) == test_result_games_count
    for games_id, games_data in test_data_games_add.items():
        await create_game(
            game_id=games_id,
            game_name=games_data["name"],
            game_cost=games_data["cost"],
            session=session,
        )
        game = await get_game_from_db(game_id=games_id, session=session)
        assert game is not None
        assert game.game_id == games_id
        assert game.name == games_data["name"]
        assert game.cost == games_data["cost"]


@pytest.mark.parametrize(
    "test_data_user,"
    "test_data_all_games,"
    "test_result_all_tracking_games_long,"
    "test_result_tracking_games_changes",
    LIST_TRACKING_GAMES_CRUD,
)
@pytest.mark.asyncio
async def test_game_track_crud(
    test_data_user: dict,
    test_data_all_games: dict,
    test_result_all_tracking_games_long: int,
    test_result_tracking_games_changes: list,
    get_game_name_mock: Callable[[Any], str],
    get_game_cost_mock: Callable[[Any], float],
    session: AsyncSession,
) -> None:
    await create_user(
        name=test_data_user["name"],
        telegram_id=test_data_user["telegram_id"],
        session=session,
    )
    for game_id, game_data in test_data_all_games.items():
        await create_game_track(
            game_id=game_id, telegram_id=test_data_user["telegram_id"], session=session
        )
        tracking_game = await get_tracking_game_from_db(
            game_id=game_id, session=session
        )
        assert tracking_game is not None
        assert tracking_game.name == game_data["name"]
        assert tracking_game.first_cost == game_data["first_cost"]
        tracking_game_data = await get_tracking_game_data_from_db(
            game_id=game_id, session=session
        )
        assert tracking_game_data == [
            (
                game_data["name"],
                game_data["first_cost"],
                game_data["first_cost"],
            )
        ]

    all_tracking_games = await get_all_tracking_games_from_db(
        telegram_id=test_data_user["telegram_id"], session=session
    )
    assert len(all_tracking_games) == test_result_all_tracking_games_long
    for game_id, game_data in test_data_all_games.items():
        await update_current_game_cost(game_id=game_id, session=session)
    tracking_games_changes = await get_tracking_games_changes(
        telegram_id=test_data_user["telegram_id"], session=session
    )
    assert tracking_games_changes == test_result_tracking_games_changes
    for game_id in test_data_all_games:
        await delete_tracking_game(game_id=game_id, session=session)
        tracking_game = await get_tracking_game_from_db(
            game_id=game_id, session=session
        )
        assert tracking_game is None
