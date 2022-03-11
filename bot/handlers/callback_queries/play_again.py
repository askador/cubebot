from typing import Union
from aiogram import Dispatcher

from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.db.models import Game
from bot.analytics import analytics
from bot.analytics.events import EventAction, EventCbQueryAction
from bot.keyboards.inline import new_game_kb
from bot.types.Localization import I18nJSON
from bot.utils.throttling import rate_limit


cd = CallbackData('game', 'action')

@rate_limit()
@analytics.cb_query(EventCbQueryAction.PLAY_AGAIN)
async def play_again(
    cb: CallbackQuery, 
    callback_data: "dict[str, Union[int, str]]", 
    i18n: I18nJSON,
    session: AsyncSession,
):
    chat_id = cb.message.chat.id

    game = (await session.execute(
        select(Game)
        .where(Game.chat_id == chat_id)
    )).fetchone()
    
    if game:
        await analytics.action(chat_id, EventAction.CALLBACK_QUERY_ANSWER)
        return await cb.answer(i18n.t('commands.game.already_exists'))

    session.add(Game(chat_id=chat_id))
    await session.commit()

    await cb.message.answer(i18n.t('commands.game.message'), reply_markup=new_game_kb(i18n.language_key))
    await cb.answer()
    await analytics.action(chat_id, EventAction.SEND_MESSAGE)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(play_again, cd.filter(action='play_again'))