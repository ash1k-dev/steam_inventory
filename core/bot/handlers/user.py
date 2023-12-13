from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.storage.redis import RedisStorage
from methods.update import update_redis
from redis_data_convert import redis_convert_to_dict
from sqlalchemy.ext.asyncio import AsyncSession


from core.bot.keyboards.inline.callback_factory import SteamidCallbackFactory
from core.bot.keyboards.inline.inline import (
    get_control_menu,
    get_steam_id_menu,
    get_steams_menu,
)
from core.bot.keyboards.reply.reply import get_main_menu, get_track_menu
from core.bot.utils.admin_notification import recording_steam_data_error
from core.db.methods.create import add_initial_data, create_user
from core.db.methods.delete import delete_steam_id
from core.db.methods.request import (
    get_all_steam_ids_from_db,
    get_steamid_from_db,
    get_user_from_db,
)
from core.inventory.steam import get_steam_id, get_steam_name

router = Router()


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
        "Главное меню",
        reply_markup=get_main_menu(),
    )


@router.message(F.text == "Мои Steam id")
async def get_steam_ids(message: Message, session: AsyncSession, storage: RedisStorage):
    telegram_id = message.from_user.id
    user_data = await redis_convert_to_dict(
        telegram_id=f"{telegram_id}", storage=storage
    )
    if user_data:
        steam_ids_list = user_data["steam_ids"]["ids"]
        steam_ids_list = [(steam_id, name) for steam_id, name in steam_ids_list.items()]
    else:
        steam_ids_list = await get_all_steam_ids_from_db(
            telegram_id=telegram_id, session=session
        )
    await message.answer(
        "Привязанные Steam ID:",
        reply_markup=get_steams_menu(steam_id_list=steam_ids_list),
    )


@router.message(F.text == "Отслеживание стоимости")
async def get_cost(message: Message):
    await message.answer("Отслеживание стоимости", reply_markup=get_track_menu())


@router.message(AddSteam.added_steam_id, flags={"long_operation": "upload_document"})
async def add_steam_id(
    message: Message,
    bot: Bot,
    session: AsyncSession,
    state: FSMContext,
    storage: RedisStorage,
):
    """Adding a steam id"""
    telegram_id = message.from_user.id
    user_data = await redis_convert_to_dict(
        telegram_id=f"{telegram_id}", storage=storage
    )
    try:
        steam_id = get_steam_id(message.text)
        steam_name = get_steam_name(steam_id)
    except Exception:
        await message.answer(text="Некорректный Stream id, попробуйте еще раз")

    else:
        if user_data:
            steam_ids = user_data["steam_ids"]
            print(steam_ids)
            check_steam_id = message.text in steam_ids
            print(check_steam_id)
        else:
            check_steam_id = await get_steamid_from_db(
                steam_id=steam_id, session=session
            )
        if check_steam_id:
            await message.answer(text="Этот Steam id уже в вашем списке")
        else:
            await message.answer(
                f"Происходит добавление steam id '{steam_id}'"
                f" с именем '{steam_name}'.\n"
                "Обработка данных займет какое-то время и зависит"
                " от количества предметов и игр на Вашем аккаунте"
            )
            try:
                await add_initial_data(
                    message=message,
                    session=session,
                    steam_id=steam_id,
                    steam_name=steam_name,
                )
                await update_redis(
                    user_telegram_id=message.from_user.id,
                    session=session,
                    storage=storage,
                )
                await message.answer(
                    f"Для Steam id '{steam_id}' с именем '{steam_name}'"
                    " данные добавлены"
                )
            except Exception as e:
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
                        "Данные о текущей ошибке отправленны администраторам"
                    )
                else:
                    await storage.redis.set(name=str(steam_id), value=1, ex=60000)
                    if check_creating_steamid:
                        await delete_steam_id(steam_id=str(steam_id), session=session)
                    await message.answer(
                        "Произошла ошибка, попробуйте повторить через 5-10 минут"
                    )

    await state.clear()


@router.callback_query(SteamidCallbackFactory.filter())
async def get_steam(
    callback: CallbackQuery,
    callback_data: SteamidCallbackFactory,
    session: AsyncSession,
    state: FSMContext,
    storage: RedisStorage,
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
        await update_redis(
            user_telegram_id=callback.from_user.id, session=session, storage=storage
        )
        await callback.message.answer(
            text=f"Steam id {callback_data.steam_id} c именем"
            f" '{callback_data.steam_name}' успешно удален"
        )
        await callback.answer()
    elif callback_data.action == "steamid":
        await callback.message.answer(
            text=f"Имя в профиле: {callback_data.steam_name} \n"
            f"Steam id: {callback_data.steam_id}",
            reply_markup=get_control_menu(
                callback_data.steam_name, callback_data.steam_id
            ),
        )
        await callback.answer()
    elif callback_data.action == "add_steam_id":
        await callback.message.answer(
            text="Введите Ваш Steam id или никнейм:",
        )
        await state.set_state(AddSteam.added_steam_id)
        await callback.answer()
