from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from core.bot.keyboards.reply import (
    get_main_menu,
    get_check_cost_menu,
)

from core.bot.keyboards.inline import get_games_menu, get_steams_menu

router = Router()


@router.message(Command(commands="start"))
async def get_start(message: Message):
    """Welcome and registration a new user"""
    await message.answer(
        f"Привет {message.from_user.full_name}", reply_markup=get_main_menu()
    )


@router.message(F.text == "Мои Steam id")
async def get_start(message: Message):
    telegram_id = message.from_user.id
    await message.answer(f"Привязанные Steam ID:", reply_markup=get_steams_menu([]))


@router.message(F.text == "Отслеживание стоимости")
async def get_start(message: Message):
    telegram_id = message.from_user.id
    await message.answer(f"Отслеживание стоимости", reply_markup=get_check_cost_menu())
