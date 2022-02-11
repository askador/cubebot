from aiogram import Dispatcher

from . import new_game

def register(dp: Dispatcher):
    new_game.register(dp)