from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker

from bot.data.config import Middlewares

from .database import DatabaseMiddleware
from .throttling import ThrottlingMiddleware
from .logging import LoggingMiddleware
from .i18n import i18nMiddleware


def setup(dp: Dispatcher, config: Middlewares, pool: sessionmaker):
    dp.middleware.setup(ThrottlingMiddleware())
    # dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(i18nMiddleware(config.i18n))
    dp.middleware.setup(DatabaseMiddleware(pool)) 