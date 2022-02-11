from asyncio.log import logger

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update

from aiogram.dispatcher.handler import CancelHandler

from bot.data.config import config

admins = config.bot.admins

class OnlyAdmins(BaseMiddleware):

    def __init__(self):
        super().__init__()

    async def on_pre_process_update(self, update: Update, data: dict):
        user_id = 0
        if update.message:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        if not user_id in admins: 
            raise CancelHandler()

 