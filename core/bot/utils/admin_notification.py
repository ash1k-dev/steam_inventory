from aiogram import Bot, Router

from config import ADMIN_ID
from core.bot.utils.templates import TEXT_STEAM_DATA_ERROR

router = Router()


@router.startup()
async def start_bot(bot: Bot) -> None:
    await bot.send_message(chat_id=ADMIN_ID, text="Бот запущен")


@router.shutdown()
async def stop_bot(bot: Bot) -> None:
    await bot.send_message(chat_id=ADMIN_ID, text="Бот остановлен")


async def send_recording_steam_data_error(
    bot: Bot, user_name: str, user_id: int, steam_id: int, error: str
) -> None:
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=TEXT_STEAM_DATA_ERROR.substitute(
            user_name=user_name,
            user_id=user_id,
            steam_id=steam_id,
            error=error,
        ),
    )
