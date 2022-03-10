from aiogram import Dispatcher

from .is_admin import IsBotAdmin
from .is_bet import IsBet
from .strict_command import StrictCommand
from .player_has_bets import PlayerHasBets
from .game_is_active import GameIsActive

def setup(dp: Dispatcher):
    dp.bind_filter(IsBotAdmin)
    dp.bind_filter(IsBet, event_handlers=[dp.message_handlers])
    dp.bind_filter(StrictCommand, event_handlers=[dp.message_handlers])
    dp.bind_filter(PlayerHasBets, event_handlers=[dp.message_handlers, dp.callback_query_handlers])
    dp.bind_filter(GameIsActive, event_handlers=[dp.message_handlers, dp.callback_query_handlers])
