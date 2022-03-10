# TODO help with specific command
# e.g. /help ставки
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from bot.filters import StrictCommand

from bot.types.Localization import I18nJSON
from bot.utils.throttling import rate_limit
from bot.analytics import analytics
from bot.analytics.events import EventAction, EventCommand


@rate_limit()
@analytics.command(EventCommand.HELP)
async def help(message: types.Message, command: Command.CommandObj, i18n: I18nJSON):
    detailed_commands_paths = {
        "ставка": "commands.help.bet"
    }

    await message.answer(i18n.t(detailed_commands_paths.get(command.args, 'commands.help.default')))
    await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)


def register(dp: Dispatcher):
    dp.register_message_handler(help, Command('help'), StrictCommand())