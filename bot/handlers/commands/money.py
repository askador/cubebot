from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from bot.db.models import Player
from bot.filters import StrictCommand
from bot.types.Localization import I18nJSON
from bot.utils.throttling import rate_limit


@rate_limit()
async def money(message: types.Message, player: Player) -> None:
    await message.reply(f"{player.money:,}")


def register(dp: Dispatcher):
    dp.register_message_handler(money, Command('money'), StrictCommand())
    dp.register_message_handler(money, Command('монеты', prefixes='!'))