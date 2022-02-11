from aiogram import Dispatcher

from . import bet

def register(dp: Dispatcher):
    bet.register(dp)