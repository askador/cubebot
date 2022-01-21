from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, CommandHelp


async def start(message: types.Message):
    await message.answer("Hello!")


async def help(message: types.Message):
    await message.answer("Help!")


def register_default_handlers(dp: Dispatcher):
    # dp.register_message_handler(start, CommandStart())
    dp.register_message_handler(help, CommandHelp())