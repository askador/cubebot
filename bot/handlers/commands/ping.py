import asyncio
from loguru import logger

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from bot.analytics import analytics
from bot.analytics.events import EventAction, EventCommand
from bot.utils.throttling import rate_limit


@rate_limit()
@analytics.command(EventCommand.PING)
async def ping(message: types.Message):
    await asyncio.sleep(5)
    await message.reply('pong')
    await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)

def register(dp: Dispatcher):
    dp.register_message_handler(ping, Command('ping'))
