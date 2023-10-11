from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession


from core.db.methods.request import (
    get_top_games_from_db,
    get_games_info_from_db,
)

from core.bot.keyboards.inline import (
    get_games_menu,
)

router = Router()


@router.callback_query(F.data.startswith("games_info"))
async def show_info_for_games(callback: CallbackQuery, session: AsyncSession):
    """Show info for current stream id"""
    games_info_data = callback.data.split("_")
    steamid_id = int(games_info_data[3])
    games_info = await get_games_info_from_db(steam_id=steamid_id, session=session)
    number_of_games, total_cost, time_in_games = games_info[0]
    await callback.message.answer(
        text=f"Количество игр на аккаунте: {number_of_games}\nОбщая стоимость игр на аккаунте: {total_cost} \nОбщее количество часов в играх: {time_in_games}",
        reply_markup=get_games_menu(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("games_list"))
async def show_top_of_games(callback: CallbackQuery, session: AsyncSession):
    """Show info for current stream id"""
    games_info_data = callback.data.split("_")
    info_type = games_info_data[2]
    if info_type == "time":
        limit = 5
        order = "time"
        title = "ТОП 5 игр в которых проведенно больше времени:"
    elif info_type == "cost":
        limit = 5
        order = "cost"
        title = "ТОП 5 самых дорогих игр:"
    elif info_type == "all":
        limit = 1000
        order = "time"
        title = "Все ваши игры в порядке количества часов:"
    top = ""
    top_games = await get_top_games_from_db(
        telegram_id=callback.from_user.id,
        limit=limit,
        order=order,
        session=session,
    )
    for game in top_games:
        top += f"Название игры: {game.game_name}.\nКоличество часов: {game.time_in_game} \nСтоимость: {game.game_cost} \n \n"
    await callback.message.answer(
        text=f"{title} \n ----------------\n{top}",
        reply_markup=get_games_menu(),
    )
    await callback.answer()
