import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from core.bot.utils import admin_notification
from core.bot.handlers import user


from config import ADMIN_ID, TOKEN
from core.inventory.steam import *

from core.bot.keyboards.reply import get_main_menu


async def get_start(message: Message):
    """"""
    await message.answer(
        f"Привет {message.from_user.full_name}", reply_markup=get_main_menu()
    )


async def send_inventory_cost(message: Message, bot: Bot):
    """"""
    try:
        inventory_cost = all_test(message.text)
        await bot.send_message(message.chat.id, text=inventory_cost)
    except Exception:
        await bot.send_message(
            message.chat.id, text="Неверный steam id, попробуйте еще раз"
        )


async def start():
    """"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )
    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_routers(user.router, admin_notification.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())
