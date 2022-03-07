from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import ChatLog
from bot.filters import StrictCommand
from bot.types.Localization import I18nJSON
from bot.utils.throttling import rate_limit
from bot.analytics import analytics
from bot.analytics.events import EventCommand, EventAction


@rate_limit()
@analytics.command(EventCommand.LOGS)
async def logs(message: types.Message, session: AsyncSession, i18n: I18nJSON):
    logs = (await session.execute(
        select([ChatLog.log])\
            .where(ChatLog.chat_id==message.chat.id)\
            .order_by(ChatLog.id)
    )).scalars().all()
    
    if not logs:
        await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)
        return await message.reply(i18n.t('commands.logs.none'))

    res = '\n'.join([f"🎲  {log}" for log in logs])
    await message.reply(res)
    await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)

def register(dp: Dispatcher):
    dp.register_message_handler(logs, Command('logs'), StrictCommand())
    dp.register_message_handler(logs, Command('логи', prefixes='!'))
