from cachetools import TTLCache

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Issue
from bot.types.Localization import I18nJSON
from bot.utils.throttling import rate_limit

ISSUE_CHAT_ID = -1001534253038
cache = TTLCache(maxsize=float('inf'), ttl=6 * 60)

@rate_limit()
async def issue(message: Message, i18n: I18nJSON, command: Command.CommandObj, session: AsyncSession):

    if cache.get(message.from_user.id):
        return await message.answer(i18n.t('commands.issue.throttle'))

    if not command.args:
        return await message.answer(i18n.t('commands.issue.rule'))

    from_user = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</>" 

    text = f"#issue\n"\
           f"От: {from_user}\n\n" \
           f"{command.args}"

    if message.photo:
        photo_id = message.photo[-1].file_id
        mes = await message.bot.send_photo(ISSUE_CHAT_ID, photo_id, caption=text)
    else:
        mes = await message.bot.send_message(ISSUE_CHAT_ID, text)
    
    session.add(Issue(link=mes.url))    
    await session.commit()
    
    await message.answer(i18n.t("commands.issue.answer"))
    cache[message.from_user.id] = True


def register(dp: Dispatcher):
    dp.register_message_handler(issue, 
        Command('issue', ignore_caption=False), 
        chat_type="private",
        content_types = ["text", "photo"]
    )