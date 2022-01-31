from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

async def ping(message: types.Message):
    await message.reply('pong')

def register(dp: Dispatcher):
    dp.register_message_handler(ping, Command('ping'))