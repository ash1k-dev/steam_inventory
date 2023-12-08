from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils import markdown
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot.utils.apsheduler import update_redis
from core.db.methods.request import (
    get_all_tracking_games_from_db,
    get_tracking_game_from_db,
    get_all_tracking_items_from_db,
    get_tracking_item_from_db,
    get_tracking_item_data_from_db,
    get_tracking_game_data_from_db,
)

from urllib.parse import quote

from aiogram.fsm.storage.redis import RedisStorage


from core.db.methods.delete import delete_tracking_game, delete_tracking_item

from core.db.methods.create import create_game_track, create_item_track

from core.inventory.steam import get_game_name, get_item_market_hash_name

from core.bot.keyboards.inline.inline import (
    get_tracking_games_menu,
    get_control_menu_tracking_game,
    get_confirm_tracking_game_menu,
    get_tracking_items_menu,
    get_control_menu_tracking_items,
    get_confirm_tracking_item_menu,
)

from core.bot.keyboards.inline.callback_factory import (
    GamesTrackCallbackFactory,
    ItemsTrackCallbackFactory,
)


import redis
import json
import ast


rs = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

router = Router()


class AddGameTrack(StatesGroup):
    """State to tracking game"""

    added_game_track = State()


class AddItemTrack(StatesGroup):
    """State to tracking game"""

    added_item_track = State()


def redis_convert_to_dict(telegram_id):
    data = rs.get(telegram_id)
    if data is not None:
        return ast.literal_eval(data)
    else:
        return False


@router.message(F.text == "Предметы")
async def get_steam_ids(message: Message, session: AsyncSession, storage: RedisStorage):
    telegram_id = message.from_user.id
    user_data = redis_convert_to_dict(f"{telegram_id}")
    if user_data:
        tracking_items = user_data["tracking_items"]
        tracking_items_list = []
        for item_id, item_data in tracking_items.items():
            tracking_items_list.append(
                (
                    item_data["name"],
                    item_id,
                    item_data["first_cost"],
                    item_data["cost"],
                )
            )
    else:
        tracking_items_list = await get_all_tracking_items_from_db(
            telegram_id=telegram_id, session=session
        )

    await message.answer(
        f"Отслеживаемые предметы:",
        reply_markup=get_tracking_items_menu(tracking_items_list=tracking_items_list),
    )


@router.message(F.text == "Игры")
async def get_steam_ids(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    user_data = redis_convert_to_dict(f"{telegram_id}")
    if user_data:
        tracking_items = user_data["tracking_games"]
        tracking_games_list = []
        for game_id, game_data in tracking_items.items():
            tracking_games_list.append(
                (
                    game_data["name"],
                    game_id,
                    game_data["first_cost"],
                    game_data["cost"],
                )
            )
    else:
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
        user_data = redis_convert_to_dict(telegram_id=callback.from_user.id)
        if user_data:
            game = user_data["tracking_games"][str(callback_data.game_id)]
        else:
            tracking_game_data = await get_tracking_game_data_from_db(
                game_id=callback_data.game_id, session=session
            )
            name, first_cost, cost = tracking_game_data[0]
            game = {"name": name, "first_cost": first_cost, "cost": cost}
        await callback.message.answer(
            text=f"{markdown.hbold(game['name'])}\n"
            f"Первоначальная стоимость: {game['first_cost']}\n"
            f"Актуальная стоимость: {game['cost']}\n"
            f"Изменение: {game['first_cost'] - game['cost']}\n"
            f"Ссылка: {markdown.hlink('SteamLink', f'https://store.steampowered.com/app/{callback_data.game_id}')}",
            reply_markup=get_control_menu_tracking_game(game_id=callback_data.game_id),
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
        await state.clear()
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
    message: Message,
    session: AsyncSession,
):
    """Adding a tracking game"""
    try:
        game = get_game_name(int(message.text))
    except Exception:
        await message.answer(text=f"Некорректный Id игры, попробуйте еще раз")

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
                reply_markup=get_confirm_tracking_game_menu(game_id=int(message.text)),
            )


@router.callback_query(ItemsTrackCallbackFactory.filter())
async def get_tracking_item(
    callback: CallbackQuery,
    callback_data: ItemsTrackCallbackFactory,
    session: AsyncSession,
    state: FSMContext,
):
    if callback_data.action == "tracking_item":
        user_data = redis_convert_to_dict(telegram_id=callback.from_user.id)
        if user_data:
            item = user_data["tracking_items"][str(callback_data.item_id)]
            name = item["name"]
        else:
            tracking_item_data = await get_tracking_item_data_from_db(
                item_id=callback_data.item_id, session=session
            )
            name, first_cost, cost = tracking_item_data[0]
            item = {"name": name, "first_cost": first_cost, "cost": cost}
            name = item["name"]
        await callback.message.answer(
            text=f"{markdown.hbold(item['name'])}\n"
            f"Первоначальная стоимость: {item['first_cost']}\n"
            f"Актуальная стоимость: {item['cost']}\n"
            f"Изменение: {item['first_cost'] - item['cost']}({int((item['first_cost'] - item['cost']) / item['first_cost'] * 100)}%)\n"
            f"Сссылка:  {markdown.hlink('SteamLink', f'https://steamcommunity.com/market/listings/730/{quote(name)}')}",
            reply_markup=get_control_menu_tracking_items(
                item_id=callback_data.item_id, item_name=item["name"]
            ),
        )

        await callback.answer()
    elif callback_data.action == "delete":
        await delete_tracking_item(item_id=callback_data.item_id, session=session)
        await callback.message.delete()
        await update_redis(user_telegram_id=callback.from_user.id, session=session)
        await callback.message.answer(text=f"Предмет успешно удален")
        await callback.answer()
    elif callback_data.action == "add_tracking_item":
        await callback.message.answer(
            text="Введите Id интересующего Вас предмета(id можно посмотреть на странице предмета в steam):",
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
        await update_redis(user_telegram_id=callback.from_user.id, session=session)
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
    message: Message,
    session: AsyncSession,
):
    """Adding a tracking game"""
    try:
        item = get_item_market_hash_name(int(message.text))
    except Exception:
        await message.answer(text=f"Некорректный Id предмета, попробуйте еще раз")

    else:
        check_game = await get_tracking_item_from_db(
            item_id=int(message.text), session=session
        )
        if check_game is not None:
            await message.answer(text=f"Предмет '{item}' уже в Вашем списке")
        else:
            await message.answer(
                f"Это Ваш предмет? \n\n"
                f"https://steamcommunity.com/market/listings/730/{quote(item)}",
                reply_markup=get_confirm_tracking_item_menu(item_id=int(message.text)),
            )
