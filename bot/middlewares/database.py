from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject
from loguru import logger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, pool):
        super(DatabaseMiddleware, self).__init__()
        self.pool: sessionmaker = pool

    async def pre_process(self, obj: TelegramObject, data: dict, *args):
        session: AsyncSession = self.pool()
        data["session"] = session

    async def post_process(self, obj: TelegramObject, data: dict, *args):
        if session := data.get('session', None):
            await session.close()
