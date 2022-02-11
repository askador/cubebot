from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from bot.filters import StrictCommand
from bot.types.Localization import I18nJSON
from bot.utils.throttling import rate_limit


@rate_limit()
async def start(message: types.Message, i18n: I18nJSON):
    await message.answer(i18n.t('commands.default.start'))

@rate_limit()
async def help(message: types.Message, i18n: I18nJSON):
    await message.answer(i18n.t('commands.default.help'))


def register(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart(), StrictCommand())
    dp.register_message_handler(help, CommandHelp(), StrictCommand())