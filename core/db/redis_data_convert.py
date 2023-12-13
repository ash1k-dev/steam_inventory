import ast

import redis

# rs = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)


async def redis_convert_to_dict(telegram_id, storage):
    data = await storage.redis.get(telegram_id)
    if data is not None:
        return ast.literal_eval(data)
    else:
        return False
