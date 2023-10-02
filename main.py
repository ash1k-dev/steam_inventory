import asyncio
import logging

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import DB_URL, TOKEN
from core.bot.handlers import user
from core.bot.middlewares.db_connection import DbConnection
from core.bot.middlewares.long_operation import LongOperationMiddleware
from core.bot.utils import admin_notification


async def start():
    """"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )
    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    engine = create_async_engine(url=DB_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    dp.message.middleware(LongOperationMiddleware())
    dp.update.middleware(DbConnection(sessionmaker))

    dp.include_routers(user.router, admin_notification.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, sessionmaker=sessionmaker)


if __name__ == "__main__":
    asyncio.run(start())
