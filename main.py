import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import DB_URL, REDIS_URL, TOKEN
from core.bot.handlers import game, item, track, user
from core.bot.middlewares.db_connection import DbConnection
from core.bot.middlewares.long_operation import LongOperationMiddleware
from core.bot.utils import admin_notification
from core.bot.utils.apsheduler import check_update


async def start():
    """"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )
    storage = RedisStorage.from_url(
        url=REDIS_URL, connection_kwargs={"decode_responses": True}
    )

    bot = Bot(token=TOKEN, parse_mode="HTML")

    dp = Dispatcher(storage=storage)

    engine = create_async_engine(url=DB_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    sheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    sheduler.add_job(
        check_update,
        trigger="interval",
        seconds=60,
        kwargs={"bot": bot, "sessionmaker": sessionmaker, "storage": storage},
    )
    sheduler.start()

    dp.update.middleware(LongOperationMiddleware())
    dp.update.middleware(DbConnection(sessionmaker))

    dp.include_routers(
        user.router, game.router, item.router, track.router, admin_notification.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, sessionmaker=sessionmaker, storage=storage)


if __name__ == "__main__":
    asyncio.run(start())
