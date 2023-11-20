from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.bot.utils.admin_notification import recording_steam_data_error
from core.db.methods.create import (
    create_user,
    add_initial_data,
)
from core.db.methods.request import (
    get_user_from_db,
    get_steamid_from_db,
    get_all_steam_ids_from_db,
)

from core.db.methods.delete import delete_steam_id

from core.bot.keyboards.reply import (
    get_main_menu,
    get_check_cost_menu,
)

from core.inventory.steam import (
    get_steam_name,
    get_steam_id,
)

from core.bot.keyboards.inline import (
    SteamidCallbackFactory,
    get_steams_menu,
    get_control_menu,
    get_steam_id_menu,
)

router = Router()
from aiogram.fsm.storage.redis import RedisStorage


class AddSteamId(StatesGroup):
    """State to user"""

    added_steam_id = State()


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
async def get_cost(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    # await update_all_items(session=session)
    await message.answer(f"Отслеживание стоимости", reply_markup=get_check_cost_menu())


@router.message(AddSteamId.added_steam_id, flags={"long_operation": "upload_document"})
async def add_steam_id(
    message: Message,
    bot: Bot,
    session: AsyncSession,
    state: FSMContext,
    storage: RedisStorage,
):
    """Adding a steam id"""
    try:
        steam_id = get_steam_id(message.text)
        steam_name = get_steam_name(steam_id)
    except Exception:
        await message.answer(text=f"Некорректный Stream ID, попробуйте еще раз")

    else:
        check_steam_id = await get_steamid_from_db(steam_id=steam_id, session=session)
        if check_steam_id is not None:
            await message.answer(text="Этот Steam ID уже в вашем списке")
        else:
            await message.answer(
                f"Происходит добавление steam id '{steam_id}' с именем '{steam_name}'.\n"
                f"Обработка данных займет какое-то время и зависит от количества предметов и игр на Вашем аккаунте"
            )
            await add_initial_data(
                    message=message,
                    session=session,
                    steam_id=steam_id,
                    steam_name=steam_name,
                )
            await message.answer(
                    f"Для Steam id '{steam_id}' с именем '{steam_name}' данные добавлены"
                )

    await state.clear()


@router.callback_query(SteamidCallbackFactory.filter())
async def get_steam(
    callback: CallbackQuery,
    callback_data: SteamidCallbackFactory,
    session: AsyncSession,
    state: FSMContext,
):
    if callback_data.action == "info":
        await callback.message.answer(
            text=f"Данные профиля {callback_data.steam_name}:",
            reply_markup=get_steam_id_menu(
                callback_data.steam_name, callback_data.steam_id
            ),
        )
        await callback.answer()
    elif callback_data.action == "delete":
        await delete_steam_id(steam_id=callback_data.steam_id, session=session)
        await callback.message.delete()
        await callback.message.answer(
            text=f"Steam ID {callback_data.steam_id} c именем '{callback_data.steam_name}' успешно удален"
        )
        await callback.answer()
    elif callback_data.action == "steamid":
        await callback.message.answer(
            text=f"Имя в профиле: {callback_data.steam_name} \nSteam ID: {callback_data.steam_id}",
            reply_markup=get_control_menu(
                callback_data.steam_name, callback_data.steam_id
            ),
        )
        await callback.answer()
    elif callback_data.action == "add_steam_id":
        await callback.message.answer(
            text="Введите Ваш Steam ID или никнейм:",
        )
        await state.set_state(AddSteamId.added_steam_id)
        await callback.answer()
