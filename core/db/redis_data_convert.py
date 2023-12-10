import redis
import ast

rs = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)


def redis_convert_to_dict(telegram_id):
    data = rs.get(telegram_id)
    if data is not None:
        return ast.literal_eval(data)
    else:
        return False
