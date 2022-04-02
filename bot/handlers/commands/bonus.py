from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command

from bot.filters import StrictCommand


async def bonus():
    ...


def register(dp: Dispatcher):
    dp.register_message_handler(bonus, Command('bonus'), StrictCommand())