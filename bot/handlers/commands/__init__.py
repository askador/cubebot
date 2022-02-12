from aiogram import Dispatcher
from . import (
    default, ping, game, bet, roll, 
    logs, money, issue, bets, cancel_bets,
    profile, give_money
)


def register(dp: Dispatcher):
    default.register(dp)
    ping.register(dp)
    game.register(dp)
    roll.register(dp)
    logs.register(dp)
    bet.register(dp)
    money.register(dp)
    issue.register(dp)
    bets.register(dp)
    cancel_bets.register(dp)
    profile.register(dp)
    give_money.register(dp)
