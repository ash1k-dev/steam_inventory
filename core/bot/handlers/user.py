from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.inventory.test_data import inventory_json

from core.db.methods.create import (
    create_user,
    create_steamid,
    create_all_games,
    create_all_steam_inventorys,
    create_all_steam_items,
    create_steam_items_in_inventory,
)
from core.db.methods.request import (
    get_user_from_db,
    get_steamid_from_db,
    check_steam_id_in_db,
    get_all_steam_ids_from_db,
    get_top_games_from_db,
    get_games_info_from_db,
    get_inventorys_id_from_db,
)
from core.db.methods.delete import delete_steam_id

from core.bot.keyboards.reply import (
    get_main_menu,
    get_check_cost_menu,
)

from core.inventory.steam import (
    get_steam_name,
    get_steam_id,
    get_all_games_info,
    get_all_inventory_info,
    get_inventory_info_test_data,
)

from core.bot.keyboards.inline import (
    get_games_menu,
    get_steams_menu,
    get_control_menu,
    get_steam_id_menu,
)

router = Router()


@router.message(Command(commands="start"))
async def get_start(message: Message, session: AsyncSession):
    """Welcome and registration a new user"""
    telegram_id = message.from_user.id
    result = await get_user_from_db(telegram_id=telegram_id, session=session)
    if result is None:
        await create_user(
            user_name=message.from_user.full_name,
            telegram_id=telegram_id,
            session=session,
        )
    await message.answer(
        f"Привет {message.from_user.full_name}",
        reply_markup=get_main_menu(),
    )


@router.message(F.text == "Мои Steam id")
async def get_steam_ids(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    steam_ids_list = await get_all_steam_ids_from_db(
        telegram_id=telegram_id, session=session
    )
    await message.answer(
        f"Привязанные Steam ID:", reply_markup=get_steams_menu(steam_ids_list)
    )


@router.message(F.text == "Отслеживание стоимости")
async def get_cost(message: Message):
    telegram_id = message.from_user.id
    await message.answer(f"Отслеживание стоимости", reply_markup=get_check_cost_menu())


class AddSteamId(StatesGroup):
    """State to add steam id"""

    added_steam_id = State()


@router.callback_query(F.data == "add_steam_id")
async def add_steam_id_text(callback: CallbackQuery, state: FSMContext):
    """Steam id adding stage"""
    await callback.message.answer(
        text="Введите Ваш Steam ID или никнейм:",
    )
    await state.set_state(AddSteamId.added_steam_id)
    await callback.answer()


@router.message(AddSteamId.added_steam_id)
async def add_steam_id(message: Message, session: AsyncSession, state: FSMContext):
    """Adding a steam id"""
    try:
        steam_id = get_steam_id(message.text)
        steam_name = get_steam_name(steam_id)
    except Exception:
        await message.answer(text=f"Некорректный Stream ID, попробуйте еще раз")

    else:
        check_steam_id = await check_steam_id_in_db(steam_id=steam_id, session=session)
        if check_steam_id is not None:
            await message.answer(text="Этот Steam ID уже в вашем списке")
        else:
            await create_steamid(
                telegram_id=message.from_user.id,
                steam_id=steam_id,
                steam_name=steam_name,
                session=session,
            )
            await message.answer(
                f"Steam id '{steam_id}' с именем '{steam_name}' успешно добавлен. \nОбработка данных займет какое-то время и зависит от количества предметов и игр на Вашем аккаунте"
            )
            all_games_info = get_all_games_info(steam_id=steam_id)
            steam_id_from_db = await get_steamid_from_db(steam_id, session=session)
            await create_all_games(
                all_games_info=all_games_info,
                steam_id=steam_id_from_db.id,
                session=session,
            )
            await create_all_steam_inventorys(
                all_games_info=all_games_info,
                steam_id=steam_id_from_db.id,
                session=session,
            )
            items_dict, classid_dict = get_inventory_info_test_data(inventory_json)
            await create_all_steam_items(items_dict, session=session)
            inventorys_id = await get_inventorys_id_from_db(session=session)
            await create_steam_items_in_inventory(
                classid_dict, inventory_id=inventorys_id.id, session=session
            )
            await message.answer(
                f"Для Steam id '{steam_id}' с именем '{steam_name}' данные добавлены"
            )

    await state.clear()


@router.callback_query(F.data.startswith("steamid_"))
async def get_current_steam_id(callback: CallbackQuery):
    """Show current steam id and keyboard"""
    steamid_name = callback.data.split("_")[1]
    steamid_id = callback.data.split("_")[2]
    await callback.message.answer(
        text=f"Имя в профиле: {steamid_name} \nSteam ID: {steamid_id}",
        reply_markup=get_control_menu(steamid_name, steamid_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("delete_"))
async def delete_current_steam_id(callback: CallbackQuery, session: AsyncSession):
    """Show current steam id and delete keyboard"""
    steamid_id = callback.data.split("_")[2]
    steamid_name = callback.data.split("_")[1]
    await delete_steam_id(steam_id=steamid_id, session=session)
    await callback.message.delete()
    await callback.message.answer(
        text=f"Steam ID {steamid_id} c именем '{steamid_name}' успешно удален"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("info_"))
async def show_info_for_current_stream_id(callback: CallbackQuery):
    """Show info for current stream id"""
    steamid_id = callback.data.split("_")[2]
    steamid_name = callback.data.split("_")[1]
    await callback.message.answer(
        text=f"Данные профиля {steamid_name}:",
        reply_markup=get_steam_id_menu(steamid_name, steamid_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("games_info"))
async def show_info_for_games(callback: CallbackQuery, session: AsyncSession):
    """Show info for current stream id"""
    games_info = await get_games_info_from_db(session=session)
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


# @router.callback_query(F.data.startswith("inventory_"))
# async def show_info_for_items(callback: CallbackQuery, session: AsyncSession):
#     """Show info for current stream id"""
#     inventory_info_data = callback.data.split("_")
#     steamid_name = inventory_info_data[1]
#     steamid_id = inventory_info_data[2]
#     total_cost = pass
#     first_total_cost = pass
#     amount = pass
#     max_cost = pass
#     min_cost = pass
#     await callback.message.answer(
#         text=f"Количество предметов на аккаунте: {amount}\nОбщая стоимость предметов на аккаунте: {total_cost} \nМаксимальная стоимость предмета: {max_cost} \nМинимальная стоимость предмета: {min_cost}",
#         reply_markup=get_games_menu(),
#     )
#     await callback.answer()
