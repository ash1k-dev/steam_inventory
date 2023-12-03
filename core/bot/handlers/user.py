from aiogram import F, Router, Bot
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

from core.bot.keyboards.reply.reply import (
    get_main_menu,
    get_track_menu,
)

from core.inventory.steam import (
    get_steam_name,
    get_steam_id,
)

from core.bot.keyboards.inline.inline import (
    get_steams_menu,
    get_control_menu,
    get_steam_id_menu,
)

from core.bot.keyboards.inline.callback_factory import SteamidCallbackFactory

router = Router()
from aiogram.fsm.storage.redis import RedisStorage


class AddSteam(StatesGroup):
    """State to user"""

    added_steam_id = State()


@router.message(F.text.in_({"/start", "Назад"}))
async def get_start(message: Message, session: AsyncSession):
    """Welcome and registration a new user"""
    telegram_id = message.from_user.id
    result = await get_user_from_db(telegram_id=telegram_id, session=session)
    if result is None:
        await create_user(
            name=message.from_user.full_name,
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
    await message.answer(f"Отслеживание стоимости", reply_markup=get_track_menu())


@router.message(AddSteam.added_steam_id, flags={"long_operation": "upload_document"})
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
            try:
                await add_initial_data(
                    message=message,
                    session=session,
                    steam_id=steam_id,
                    steam_name=steam_name,
                )
                await message.answer(
                    f"Для Steam id '{steam_id}' с именем '{steam_name}' данные добавлены"
                )
            except BaseException as e:
                check_earlier_error = await storage.redis.get(name=str(steam_id))
                check_creating_steamid = await get_steamid_from_db(
                    steam_id=steam_id, session=session
                )
                if check_earlier_error:
                    await recording_steam_data_error(
                        bot=bot,
                        user_name=message.from_user.full_name,
                        user_id=message.from_user.id,
                        steam_id=steam_id,
                        error=e,
                    )
                    if check_creating_steamid:
                        await delete_steam_id(steam_id=str(steam_id), session=session)
                    await storage.redis.delete(str(steam_id))
                    await message.answer(
                        f"Данные о текущей ошибке отправленны администраторам"
                    )
                else:
                    await storage.redis.set(name=str(steam_id), value=1, ex=60000)
                    if check_creating_steamid:
                        await delete_steam_id(steam_id=str(steam_id), session=session)
                    await message.answer(
                        f"Произошла ошибка, попробуйте повторить через 5-10 минут"
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
        await state.set_state(AddSteam.added_steam_id)
        await callback.answer()
