from aiogram import Bot, Router

from config import ADMIN_ID

router = Router()


@router.startup()
async def start_bot(bot: Bot):
    """Sending message about start bot"""
    await bot.send_message(chat_id=ADMIN_ID, text="Бот запущен")


@router.shutdown()
async def stop_bot(bot: Bot):
    """Sending message about stop bot"""
    await bot.send_message(chat_id=ADMIN_ID, text="Бот остановлен")
