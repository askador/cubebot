from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from bot.db.models import Player
from bot.types.Localization import I18nJSON
from bot.filters import StrictCommand
from bot.analytics import analytics
from bot.analytics.events import EventAction, EventCommand

@analytics.command(EventCommand.PROFILE)
async def profile(message: Message, player: Player, i18n: I18nJSON):
    profile = i18n.t('commands.profile', {
        "id": player.id,
        "name": player.fullname,
        "money": f"{player.money:,}",
        "won": f"{player.won:,}",
        "loss": f"{player.loss:,}",
        "plays_amount": f"{player.plays_amount:,}",
    })
            
    await message.reply(profile)
    await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)
            
            
def register(dp: Dispatcher):
    dp.register_message_handler(profile, Command('profile'), StrictCommand())
            

    
