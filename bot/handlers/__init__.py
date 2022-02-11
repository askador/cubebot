from aiogram import Dispatcher

from . import errors, commands, chat_migration, callback_queries

def setup(dp: Dispatcher):
    errors.register(dp)
    commands.register(dp)
    chat_migration.register(dp)
    callback_queries.register(dp)
    