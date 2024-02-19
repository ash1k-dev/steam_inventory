import ast

from aiogram.fsm.storage.redis import RedisStorage


async def redis_convert_to_dict(telegram_id: int, storage: RedisStorage) -> bool | dict:
    """Конвертация данных из Redis в словарь"""
    data = await storage.redis.get(str(telegram_id))
    if data is not None:
        return ast.literal_eval(data)
    else:
        return False
