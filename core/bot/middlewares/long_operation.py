from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from config import TOKEN

bot = Bot(token=TOKEN, parse_mode="HTML")


class LongOperationMiddleware(BaseMiddleware):
    """Long loading effect"""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        long_operation_type = get_flag(data, "long_operation")

        if not long_operation_type:
            return await handler(event, data)

        async with ChatActionSender(
            bot=bot, action=long_operation_type, chat_id=event.chat.id
        ):
            return await handler(event, data)
