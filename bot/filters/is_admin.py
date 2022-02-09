from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.data.config import config

admins = config.bot.admins
 
class IsBotAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in admins
