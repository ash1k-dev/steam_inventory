from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.methods.request import (
    get_all_tracking_games_from_db,
    get_tracking_game_from_db,
)

from core.db.methods.delete import delete_tracking_game

from core.db.methods.create import create_game_track

from core.inventory.steam import get_game_name

from core.bot.keyboards.inline import (
    GamesTrackCallbackFactory,
    get_tracking_games_menu,
    get_control_menu_tracking_game,
    get_confirm_tracking_games_menu,
)

router = Router()


class AddGameTrack(StatesGroup):
    """State to tracking game"""

    added_game_track = State()
    confirm_game_track = State()


@router.message(F.text == "Игры")
async def get_steam_ids(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    tracking_games_list = await get_all_tracking_games_from_db(
        telegram_id=telegram_id, session=session
    )
    await message.answer(
        f"Отслеживаемые игры:",
        reply_markup=get_tracking_games_menu(tracking_games_list=tracking_games_list),
    )


@router.callback_query(GamesTrackCallbackFactory.filter())
async def get_tracking_games(
    callback: CallbackQuery,
    callback_data: GamesTrackCallbackFactory,
    session: AsyncSession,
    state: FSMContext,
):
    if callback_data.action == "tracking_game":
        await callback.message.answer(
            text=f"{markdown.hbold(callback_data.name)}\n"
            f"Первоначальная стоимость: {callback_data.first_game_cost}\n"
            f"Актуальная стоимость: {callback_data.game_cost}",
            reply_markup=get_control_menu_tracking_game(
                game_id=callback_data.game_id, game_name=callback_data.name
            ),
        )
        await callback.answer()
    elif callback_data.action == "delete":
        await delete_tracking_game(game_id=callback_data.game_id, session=session)
        await callback.message.delete()
        await callback.message.answer(text=f"Игра {callback_data.name} успешно удалена")
        await callback.answer()
    elif callback_data.action == "add_tracking_game":
        await callback.message.answer(
            text="Введите Id интересующей Вас игры(id можно посмотреть на странице игры в steam):",
        )
        await state.set_state(AddGameTrack.added_game_track)
        await callback.answer()
    elif callback_data.action == "add_tracking_game_confirm":
        await create_game_track(
            game_id=callback_data.game_id,
            telegram_id=callback.from_user.id,
            session=session,
        )
        await callback.message.answer(
            text="Игра успешно добавлена",
        )
        await callback.answer()
    elif callback_data.action == "add_tracking_game_not_confirm":
        await callback.message.answer(
            text="Попробуйте еще раз:",
        )
        await state.set_state(AddGameTrack.added_game_track)
        await callback.answer()


@router.message(AddGameTrack.added_game_track)
async def add_steam_id(
    message: Message,
    session: AsyncSession,
):
    """Adding a tracking game"""
    try:
        game = get_game_name(int(message.text))
    except Exception:
        await message.answer(text=f"Некорректный ID игры, попробуйте еще раз")

    else:
        check_game = await get_tracking_game_from_db(
            game_id=int(message.text), session=session
        )
        if check_game is not None:
            await message.answer(text=f"Игра '{game}' уже в вашем списке")
        else:
            await message.answer(
                f"Это Ваша игра? \n\n"
                f"https://store.steampowered.com/app/{int(message.text)}",
                reply_markup=get_confirm_tracking_games_menu(game_id=int(message.text)),
            )
