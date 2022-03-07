from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from bot.filters import StrictCommand
from bot.types.Localization import I18nJSON
from bot.utils.throttling import rate_limit
from bot.analytics import analytics
from bot.analytics.events import EventAction, EventCommand


@rate_limit()
@analytics.command(EventCommand.START)
async def start(message: types.Message, i18n: I18nJSON):
    await message.answer(i18n.t('commands.default.start'))
    await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)


@rate_limit()
@analytics.command(EventCommand.HELP)
async def help(message: types.Message, i18n: I18nJSON):
    await message.answer(i18n.t('commands.default.help'))
    await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)


def register(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart(), StrictCommand())
    dp.register_message_handler(help, CommandHelp(), StrictCommand())
