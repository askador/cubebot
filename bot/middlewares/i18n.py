from asyncio.log import logger

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from bot.types import I18nJSON
from bot.data.config import I18nConfig

class i18nMiddleware(BaseMiddleware):

    def __init__(self, config: I18nConfig):
        super(i18nMiddleware, self).__init__()
        self.i18n = I18nJSON(config)


    async def on_process_message(self, message: Message, data: dict):
        locale = message.from_user.language_code

        self.i18n.set_language(locale)
        data['i18n'] = self.i18n
