import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMIN_ID, TOKEN
from core.inventory.steam import *


async def get_start(message: Message):
    """"""
    await message.answer(f"Привет {message.from_user.full_name}")


async def start_bot(bot: Bot):
    """"""
    await bot.send_message(chat_id=ADMIN_ID, text="Бот запущен")


async def stop_bot(bot: Bot):
    """"""
    await bot.send_message(chat_id=ADMIN_ID, text="Бот остановлен")


async def send_inventory_cost(message: Message, bot: Bot):
    """"""
    try:
        inventory_cost = all_test(message.text)
        await bot.send_message(message.chat.id, text=inventory_cost)
    except Exception:
        await bot.send_message(
            message.chat.id, text="Неверный id, попробуйте еще раз"
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

    dp.message.register(get_start, Command(commands=["run", "start"]))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(send_inventory_cost)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())