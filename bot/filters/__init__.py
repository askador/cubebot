from aiogram import Dispatcher

from .is_admin import IsBotAdmin
from .is_bet import IsBet
from .strict_command import StrictCommand
from .can_roll import CanRoll

def setup(dp: Dispatcher):
    dp.bind_filter(IsBotAdmin)
    dp.bind_filter(IsBet, event_handlers=[dp.message_handlers])
    dp.bind_filter(StrictCommand, event_handlers=[dp.message_handlers])
    dp.bind_filter(CanRoll, event_handlers=[dp.message_handlers])