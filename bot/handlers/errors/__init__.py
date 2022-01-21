from aiogram import Dispatcher
from aiogram.utils import exceptions

from .error_master import errors_handler

def register_errors_handlers(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)