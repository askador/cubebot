from math import inf
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from cachetools import TTLCache

THROTTLE_TIME_DEFAULT = 1    # время искусственной задержки между остальными командами, оно же период троттлинга
THROTTLE_TIME_ROLL = 2     # время искусственной задержки между броском дайса и ответом, оно же период троттлинга
THROTTLE_TIME_BET = 0.8      # время искусственной задержки между ставкой и ответом, оно же период троттлинга

# Разные по продолжительности кэши для разных типов действий (запуск игрового автомата или /-команды)
caches = {
    "default": TTLCache(maxsize=inf, ttl=THROTTLE_TIME_DEFAULT),
    "roll": TTLCache(maxsize=inf, ttl=THROTTLE_TIME_ROLL),
    "bet": TTLCache(maxsize=inf, ttl=THROTTLE_TIME_BET),
}


# Этот мидлварь ссылается на throttling_key хендлера
class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self):
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        handler = current_handler.get()
        throttling_key = getattr(handler, 'throttling_key', None)

        if throttling_key and throttling_key in caches:
            if not caches[throttling_key].get(user_id):
                caches[throttling_key][user_id] = True
                return
            else:
                raise CancelHandler