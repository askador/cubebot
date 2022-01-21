from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject
from sqlalchemy.orm import Session, sessionmaker


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, pool):
        super(DatabaseMiddleware, self).__init__()
        self.pool: sessionmaker = pool

    async def pre_process(self, obj: TelegramObject, data: dict, *args):
        session: Session = self.pool()
        data["session"] = session

    async def post_process(self, obj: TelegramObject, data: dict, *args):
        if session := data.get('session', None):
            await session.close()