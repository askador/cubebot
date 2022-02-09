from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import ChatLog
from bot.types.Localization import I18nJSON
from bot.utils.throttling import rate_limit

@rate_limit()
async def logs(message: types.Message, session: AsyncSession, i18n: I18nJSON):
    logs = (await session.execute(
        select([ChatLog.log]).where(ChatLog.chat_id==message.chat.id).order_by(ChatLog.id)
    )).scalars().all()
    
    if not logs:
        return await message.reply(i18n.t('commands.logs.none'))

    res = '\n'.join([f"🎲  {log}" for log in logs])
    await message.reply(res)

def register(dp: Dispatcher):
    dp.register_message_handler(logs, Command('logs'))
    dp.register_message_handler(logs, Command('логи', prefixes='!'))