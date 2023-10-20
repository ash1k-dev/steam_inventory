from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession


from core.db.methods.request import (
    get_top_games_from_db,
    get_games_info_from_db,
)

from core.bot.keyboards.inline import (
    get_games_menu,
    get_games_back_menu,
    get_pagination,
)

from core.bot.keyboards.inline import GamesCallbackFactory


router = Router()


@router.callback_query(GamesCallbackFactory.filter())
async def test_change(
    callback: CallbackQuery, callback_data: GamesCallbackFactory, session: AsyncSession
):
    if callback_data.action == "info" or callback_data.action == "back":
        steamid_id = int(callback_data.steam_id)
        games_info = await get_games_info_from_db(steam_id=steamid_id, session=session)
        number_of_games, total_cost, time_in_games = games_info[0]
        await callback.message.answer(
            text=f"Количество игр на аккаунте: {number_of_games}\n"
            f"Общая стоимость игр на аккаунте: {total_cost}\n"
            f"Общее количество часов в играх: {time_in_games}",
            reply_markup=get_games_menu(
                steam_id=callback_data.steam_id, steam_name=callback_data.steam_name
            ),
        )
    else:
        if callback_data.action == "time":
            all_games = await get_top_games_from_db(
                telegram_id=callback.from_user.id,
                limit=callback_data.limit,
                order=callback_data.order,
                session=session,
            )
        elif callback_data.action == "cost":
            all_games = await get_top_games_from_db(
                telegram_id=callback.from_user.id,
                limit=callback_data.limit,
                order=callback_data.order,
                session=session,
            )
        elif callback_data.action == "all":
            all_games = await get_top_games_from_db(
                telegram_id=callback.from_user.id,
                limit=callback_data.limit,
                order=callback_data.order,
                session=session,
            )
        games = []
        for game in all_games:
            games.append(
                f"Название игры: {game.game_name}\n"
                f"Количество часов: {game.time_in_game}\n"
                f"Стоимость: {game.game_cost}\n\n"
            )
        if len(games) <= 5:
            await callback.message.answer(
                text=f"{''.join(games)}",
                reply_markup=get_games_back_menu(
                    steam_id=callback_data.steam_id, steam_name=callback_data.steam_name
                ),
            )
        else:
            await callback.message.edit_text(
                text=f"{games[callback_data.page]}",
                disable_webpage_preview=True,
                reply_markup=get_pagination(
                    action="all",
                    callbackfactory=GamesCallbackFactory,
                    page=callback_data.page,
                    pages_amount=callback_data.pages_amount,
                    steam_id=callback_data.steam_id,
                    steam_name=callback_data.steam_name,
                    limit=callback_data.limit,
                    order=callback_data.order,
                ),
            )
    await callback.answer()
