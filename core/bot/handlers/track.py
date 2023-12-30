from urllib.parse import quote

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown
from sqlalchemy.ext.asyncio import AsyncSession

from config import URL_FOR_STEAM_GAME, URL_FOR_STEAM_ITEM
from core.bot.handlers.templates import (
    TEXT_TRACKING_GAME,
    TEXT_TRACKING_GAME_CHECK,
    TEXT_TRACKING_ITEM,
    TEXT_TRACKING_ITEM_CHECK,
)
from core.bot.keyboards.inline.callback_factory import (
    GamesTrackCallbackFactory,
    ItemsTrackCallbackFactory,
)
from core.bot.keyboards.inline.inline import (
    get_confirm_tracking_game_menu,
    get_confirm_tracking_item_menu,
    get_control_menu_tracking_game,
    get_control_menu_tracking_items,
    get_tracking_games_menu,
    get_tracking_items_menu,
)
from core.bot.utils.apsheduler import update_redis
from core.db.methods.create import create_game_track, create_item_track
from core.db.methods.delete import delete_tracking_game, delete_tracking_item
from core.db.methods.request import (
    check_game_exist_in_redis_or_db,
    check_item_exist_in_redis_or_db,
    get_tracking_game_from_redis_or_db,
    get_tracking_games_list_from_redis_or_db,
    get_tracking_item_from_redis_or_db,
    get_tracking_items_list_from_redis_or_db,
)
from core.inventory.steam import get_game_name, get_item_market_hash_name

router = Router()


class AddGameTrack(StatesGroup):
    added_game_track = State()


class AddItemTrack(StatesGroup):
    added_item_track = State()


@router.message(F.text == "Предметы")
async def get_tracking_items(
    message: Message, session: AsyncSession, storage: RedisStorage
):
    tracking_items_list = await get_tracking_items_list_from_redis_or_db(
        session=session, telegram_id=message.from_user.id, storage=storage
    )
    await message.answer(
        "Отслеживаемые предметы:",
        reply_markup=get_tracking_items_menu(tracking_items_list=tracking_items_list),
    )


@router.message(F.text == "Игры")
async def get_tracking_games(
    message: Message, session: AsyncSession, storage: RedisStorage
):
    tracking_games_list = await get_tracking_games_list_from_redis_or_db(
        session=session, telegram_id=message.from_user.id, storage=storage
    )
    await message.answer(
        "Отслеживаемые игры:",
        reply_markup=get_tracking_games_menu(tracking_games_list=tracking_games_list),
    )


@router.callback_query(GamesTrackCallbackFactory.filter())
async def get_tracking_games(
    callback: CallbackQuery,
    callback_data: GamesTrackCallbackFactory,
    session: AsyncSession,
    state: FSMContext,
    storage: RedisStorage,
):
    if callback_data.action == "tracking_game":
        game = await get_tracking_game_from_redis_or_db(
            telegram_id=callback.from_user.id,
            callback_data=callback_data,
            session=session,
            storage=storage,
        )
        await callback.message.answer(
            text=TEXT_TRACKING_GAME.substitute(
                name=game["name"],
                cost=game["cost"],
                first_cost=game["first_cost"],
                difference=game["cost"] - game["first_cost"],
                link=markdown.hlink(
                    "SteamLink", f"{URL_FOR_STEAM_GAME}{callback_data.game_id}"
                ),
            ),
            reply_markup=get_control_menu_tracking_game(game_id=callback_data.game_id),
        )
        await callback.answer()
    elif callback_data.action == "delete":
        await delete_tracking_game(game_id=callback_data.game_id, session=session)
        await callback.message.delete()
        await update_redis(
            user_telegram_id=callback.from_user.id, session=session, storage=storage
        )
        await callback.message.answer(text="Игра успешно удалена")
        await callback.answer()
    elif callback_data.action == "add_tracking_game":
        await callback.message.answer(
            text="Введите Id интересующей Вас игры(id можно посмотреть"
            " на странице игры в steam):",
        )
        await state.set_state(AddGameTrack.added_game_track)
        await callback.answer()
    elif callback_data.action == "add_tracking_game_confirm":
        await create_game_track(
            game_id=callback_data.game_id,
            telegram_id=callback.from_user.id,
            session=session,
        )
        await state.clear()
        await update_redis(
            user_telegram_id=callback.from_user.id, session=session, storage=storage
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
async def add_tracking_games(
    message: Message, session: AsyncSession, storage: RedisStorage
):
    try:
        game = get_game_name(int(message.text))
    except Exception:
        await message.answer(text="Некорректный Id игры, попробуйте еще раз")

    else:
        check_game = await check_game_exist_in_redis_or_db(
            telegram_id=message.from_user.id,
            game_id=message.text,
            session=session,
            storage=storage,
        )
        if check_game:
            await message.answer(text=f"Игра '{game}' уже в вашем списке")
        else:
            await message.answer(
                text=TEXT_TRACKING_GAME_CHECK.substitute(
                    link=f"{URL_FOR_STEAM_GAME}{int(message.text)}"
                ),
                reply_markup=get_confirm_tracking_game_menu(game_id=int(message.text)),
            )


@router.callback_query(ItemsTrackCallbackFactory.filter())
async def get_tracking_item(
    callback: CallbackQuery,
    callback_data: ItemsTrackCallbackFactory,
    session: AsyncSession,
    state: FSMContext,
    storage: RedisStorage,
):
    if callback_data.action == "tracking_item":
        item, name = await get_tracking_item_from_redis_or_db(
            telegram_id=callback.from_user.id,
            callback_data=callback_data,
            session=session,
            storage=storage,
        )
        await callback.message.answer(
            text=TEXT_TRACKING_ITEM.substitute(
                name=name,
                cost=item["cost"],
                first_cost=item["first_cost"],
                difference=item["cost"] - item["first_cost"],
                difference_percents=int(
                    (item["cost"] - item["first_cost"]) / item["first_cost"] * 100
                ),
                link=markdown.hlink("SteamLink", f"{URL_FOR_STEAM_ITEM}{quote(name)}"),
            ),
            reply_markup=get_control_menu_tracking_items(item_id=callback_data.item_id),
        )

        await callback.answer()
    elif callback_data.action == "delete":
        await delete_tracking_item(item_id=callback_data.item_id, session=session)
        await callback.message.delete()
        await update_redis(
            user_telegram_id=callback.from_user.id, session=session, storage=storage
        )
        await callback.message.answer(text="Предмет успешно удален")
        await callback.answer()
    elif callback_data.action == "add_tracking_item":
        await callback.message.answer(
            text="Введите Id интересующего Вас предмета"
            "(id можно посмотреть на странице предмета в steam):",
        )
        await state.set_state(AddItemTrack.added_item_track)
        await callback.answer()
    elif callback_data.action == "add_tracking_item_confirm":
        await create_item_track(
            item_id=callback_data.item_id,
            telegram_id=callback.from_user.id,
            session=session,
        )
        await state.clear()
        await update_redis(
            user_telegram_id=callback.from_user.id, session=session, storage=storage
        )
        await callback.message.answer(
            text="Предмет успешно добавлен",
        )
        await callback.answer()
    elif callback_data.action == "add_tracking_item_not_confirm":
        await callback.message.answer(
            text="Попробуйте еще раз:",
        )
        await state.set_state(AddItemTrack.added_item_track)
        await callback.answer()


@router.message(AddItemTrack.added_item_track)
async def add_tracking_item(
    message: Message, session: AsyncSession, storage: RedisStorage
):
    try:
        item = get_item_market_hash_name(int(message.text))
    except Exception:
        await message.answer(text="Некорректный Id предмета, попробуйте еще раз")

    else:
        check_game = await check_item_exist_in_redis_or_db(
            telegram_id=message.from_user.id,
            item_id=message.text,
            session=session,
            storage=storage,
        )
        if check_game:
            await message.answer(text=f"Предмет '{item}' уже в Вашем списке")
        else:
            await message.answer(
                text=TEXT_TRACKING_ITEM_CHECK.substitute(
                    link=f"{URL_FOR_STEAM_ITEM}{quote(item)}"
                ),
                reply_markup=get_confirm_tracking_item_menu(item_id=int(message.text)),
            )
