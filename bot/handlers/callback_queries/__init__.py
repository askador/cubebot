from aiogram import Dispatcher

from . import bet, roll

def register(dp: Dispatcher):
    bet.register(dp)
    roll.register(dp)
