from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker

from bot.data.config import I18nConfig

from .acl import ACLMiddleware
from .database import DatabaseMiddleware
from .throttling import ThrottlingMiddleware
from .logging import LoggingMiddleware
from .i18n import i18nMiddleware
from .only_admins import OnlyAdmins


def setup(dp: Dispatcher, i18n: I18nConfig, pool: sessionmaker, is_dev: bool = False):
    if is_dev:
        dp.middleware.setup(OnlyAdmins())           # pre_process
    dp.middleware.setup(DatabaseMiddleware(pool))   # pre_process
    dp.middleware.setup(ACLMiddleware())            # pre_process
    dp.middleware.setup(LoggingMiddleware())        
    dp.middleware.setup(ThrottlingMiddleware())     # process   note: not pre_process bc it cannot get access to throttle key
    dp.middleware.setup(i18nMiddleware(i18n))       # process
