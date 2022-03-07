from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Issue
from bot.analytics import analytics
from bot.analytics.events import EventAction, EventCommand
from bot.types.Localization import I18nJSON
from bot.utils import rate_limit, redis_storage


ISSUE_CHAT_ID = -1001534253038
ONE_HOUR = 60 * 60
SIX_HOURS = 6 * ONE_HOUR

@rate_limit()
@analytics.command(EventCommand.ISSUE)
async def issue(
    message: Message, 
    i18n: I18nJSON, 
    command: Command.CommandObj, 
    session: AsyncSession
):

    if await redis_storage.get(prefix="issue", user=message.from_user.id):
        await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)
        return await message.answer(i18n.t('commands.issue.throttle'))

    # if await redis_storage.get(prefix="issue", user=message.from_user.id):
    #     return await message.answer("CACHED")

    if not command.args:
        await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)
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
    await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)
    

    session.add(Issue(link=mes.url))    
    await session.commit()
    
    await message.answer(i18n.t("commands.issue.answer"))
    await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)
    
    await redis_storage.set(prefix="issue", user=message.from_user.id, data="used", ttl=SIX_HOURS)



def register(dp: Dispatcher):
    dp.register_message_handler(issue, 
        Command('issue', ignore_caption=False), 
        chat_type="private",
        content_types = ["text", "photo"]
    )
