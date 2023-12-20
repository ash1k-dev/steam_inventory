from aiogram import Router
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from aiogram.utils import markdown


from config import ITEMS_ON_PAGE
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot.keyboards.inline.callback_factory import GamesCallbackFactory
from core.bot.keyboards.inline.inline import (
    get_games_back_menu,
    get_games_menu,
    get_pagination,
)
from core.db.methods.request import (
    get_games_list_from_redis_or_db,
    get_games_info_from_redis_or_db,
)

router = Router()


@router.callback_query(GamesCallbackFactory.filter())
async def get_games(
    callback: CallbackQuery,
    callback_data: GamesCallbackFactory,
    session: AsyncSession,
    storage: RedisStorage,
):
    if callback_data.action == "info" or callback_data.action == "back":
        (
            number_of_games,
            time_in_games,
            total_cost,
        ) = await get_games_info_from_redis_or_db(
            callback_data=callback_data,
            telegram_id=callback.from_user.id,
            session=session,
            storage=storage,
        )
        await callback.message.answer(
            text=f"{markdown.hbold('Аккаунт ' + callback_data.steam_name)}\n"
            f"Количество: {number_of_games}\n"
            f"Общая стоимость: {total_cost}\n"
            f"Общее количество часов: {time_in_games}",
            reply_markup=get_games_menu(
                steam_id=callback_data.steam_id, steam_name=callback_data.steam_name
            ),
        )
    else:
        if callback_data.action == "time":
            games_list = await get_games_list_from_redis_or_db(
                callback_data=callback_data,
                telegram_id=callback.from_user.id,
                storage=storage,
                session=session,
                order="time_in_game",
            )
        elif callback_data.action == "cost":
            games_list = await get_games_list_from_redis_or_db(
                callback_data=callback_data,
                telegram_id=callback.from_user.id,
                storage=storage,
                session=session,
                order="cost",
            )
        elif callback_data.action == "all":
            games_list = await get_games_list_from_redis_or_db(
                callback_data=callback_data,
                telegram_id=callback.from_user.id,
                storage=storage,
                session=session,
                order="cost",
            )
        games_list, grouped_games_list = await get_games_text(games_list)
        if len(games_list) <= ITEMS_ON_PAGE:
            await callback.message.answer(
                text=f"{''.join(games_list)}",
                disable_web_page_preview=True,
                reply_markup=get_games_back_menu(
                    steam_id=callback_data.steam_id, steam_name=callback_data.steam_name
                ),
            )
        else:
            await callback.message.edit_text(
                text=f"{grouped_games_list[callback_data.page]}",
                disable_web_page_preview=True,
                reply_markup=get_pagination(
                    action="all",
                    callbackfactory=GamesCallbackFactory,
                    page=callback_data.page,
                    pages_amount=len(grouped_games_list),
                    steam_id=callback_data.steam_id,
                    steam_name=callback_data.steam_name,
                    limit=callback_data.limit,
                    order=callback_data.order,
                ),
            )
    await callback.answer()


async def get_games_text(all_games) -> tuple[list, list]:
    games_list = []
    grouped_games_list = []
    for game_id, game_name, first_game_cost, time_in_game, game_cost in all_games:
        games_list.append(
            f"{markdown.hbold(game_name)}\n"
            f"Количество часов: {time_in_game}\n"
            f"Актуальная стоимость: {game_cost}\n"
            f"Первоначальная стоимость: {first_game_cost}\n"
            f"Ссылка на торговую площадку: "
            f"{markdown.hlink('SteamLink', f'https://store.steampowered.com/app/{game_id}')}\n\n"
        )
    for i in range(0, len(games_list), ITEMS_ON_PAGE):
        grouped_games_list.append("".join(games_list[i : i + ITEMS_ON_PAGE]))
    return games_list, grouped_games_list
