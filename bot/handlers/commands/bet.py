from typing import Optional

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Player, Game, Bet
from bot.filters import IsBet
from bot.types.Localization import I18nJSON
from bot.utils import rate_limit
from bot.analytics import analytics
from bot.analytics.events import EventAction, EventCommand


@rate_limit(key="bet")
@analytics.command(EventCommand.BET)
async def bet(
    message: types.Message, 
    i18n: I18nJSON, 
    session: AsyncSession, 
    player: Player, 
    bets: list[tuple[int, str]]
):
    chat_id = message.chat.id
    total_amount: int = sum(int(a) for a, n in bets)

    if player.money < total_amount:
        return await message.reply(i18n.t('money.not_enough')) 

    results = ''

    for bet in bets:
        amount, numbers = int(bet[0]), bet[1]
        session.add(Bet(
            player_id=player.id,
            chat_id=chat_id,
            amount=amount,
            numbers=numbers
        ))
        player.money -= amount  # type: ignore

        results += i18n.t(
            'commands.bet', 
            {
                "id": player.id,
                "name": player.fullname,
                "amount": f"{amount:,}",
                "numbers": numbers   
            },
            amount = amount
        ) + '\n'
        
    await session.commit()

    await message.answer(results)
    await analytics.action(chat_id, EventAction.SEND_MESSAGE)

def register(dp: Dispatcher):
    dp.register_message_handler(bet, Command(['ставка', 'с'], prefixes='!'), IsBet())
