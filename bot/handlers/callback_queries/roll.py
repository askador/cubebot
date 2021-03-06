import asyncio

from typing import Union
from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from bot.analytics import analytics, events
from bot.filters import PlayerHasBets, GameIsActive
from bot.db.models import Player, Game
from bot.types.Localization import I18nJSON
from bot.handlers.commands.roll import process_bets
from bot.keyboards.inline import play_again_kb

cd = CallbackData('game', 'action')

@analytics.cb_query(events.EventCbQueryAction.ROLL)
async def cb_roll(
    cb: CallbackQuery, 
    callback_data: "dict[str, Union[int, str]]", 
    i18n: I18nJSON,
    session: AsyncSession,
    no_bets: bool = False
):
    chat_id = cb.message.chat.id

    if no_bets:
        await analytics.action(chat_id, events.EventAction.CALLBACK_QUERY_ANSWER)
        return await cb.answer(i18n.t('commands.roll.invalid'))


    await session.execute(update(Game).where(Game.chat_id == chat_id).values({"is_rolling": True}))
    await session.commit()
    await cb.answer()

    dice_msg = await cb.message.answer_dice("🎲")
    await analytics.action(chat_id, events.EventAction.SEND_MESSAGE)
    number = dice_msg.dice.value

    results = f'🎲  {number}\n'
    await asyncio.sleep(4)
    results += await process_bets(number, chat_id, session, i18n)

    await cb.message.answer(results, reply_markup=play_again_kb(i18n.language_key))
    await analytics.action(chat_id, events.EventAction.SEND_MESSAGE)



def register(dp: Dispatcher):
    dp.register_callback_query_handler(cb_roll, cd.filter(action='roll'), GameIsActive(), PlayerHasBets())
