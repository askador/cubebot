from aiogram import Dispatcher

from . import bet, roll, play_again

def register(dp: Dispatcher):
    bet.register(dp)
    roll.register(dp)
    play_again.register(dp)
