from aiogram import Dispatcher
from . import (
    help, ping, game, bet, roll, 
    logs, money, issue, cancel_bets,
    profile, give_money, show_bets,
    start
)


def register(dp: Dispatcher):
    start.register(dp)
    help.register(dp)
    ping.register(dp)
    game.register(dp)
    roll.register(dp)
    logs.register(dp)
    bet.register(dp)
    money.register(dp)
    issue.register(dp)
    show_bets.register(dp)
    cancel_bets.register(dp)
    profile.register(dp)
    give_money.register(dp)
