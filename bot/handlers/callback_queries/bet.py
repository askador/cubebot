from typing import Optional, Union
from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.analytics import analytics, events
from bot.analytics.events import EventAction
from bot.db.models import Bet, Game, Player
from bot.filters.game_is_active import GameIsActive
from bot.types.Localization import I18nJSON

cd = CallbackData('game', 'action', 'amount', 'number')

@analytics.cb_query(events.EventCbQueryAction.BET)
async def bet(
    cb: CallbackQuery, 
    callback_data: "dict[str, Union[int, str]]", 
    i18n: I18nJSON,
    player: Player, 
    session: AsyncSession
):
    chat_id = cb.message.chat.id
    amount = int(callback_data["amount"])
    number = callback_data["number"]


    if not player.money >= amount:
        await analytics.action(chat_id, EventAction.CALLBACK_QUERY_ANSWER)
        return await cb.answer(i18n.t('money.not_enough')) 

    await session.execute(
        update(Player)
        .where(Player.id == player.id)
        .values({"money": player.money - amount}) 
    )

    session.add(Bet(
        player_id=player.id,
        chat_id=chat_id,
        amount=amount,
        numbers=number
    ))
    await session.commit()
    await cb.answer()

    await cb.message.answer(i18n.t(
        'commands.bet', 
        {
            "id": player.id,
            "name": player.fullname,
            "amount": f"{amount:,}",
            "numbers": number   
        },
        amount = amount
    ))
    await analytics.action(cb.message.chat.id, EventAction.SEND_MESSAGE)
    

    await analytics.action(cb.message.chat.id,EventAction.CALLBACK_QUERY_ANSWER)

def register(dp: Dispatcher):
    dp.register_callback_query_handler(bet, cd.filter(action='bet'), GameIsActive())
