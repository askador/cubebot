from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from sqlalchemy import func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Player, Bet
from bot.types.Localization import I18nJSON
from bot.utils import rate_limit
from bot.analytics import analytics
from bot.analytics.events import EventAction, EventCommand


@rate_limit(key="bet")
@analytics.command(EventCommand.PING)
async def show_bets(
    message: types.Message, 
    i18n: I18nJSON, 
    session: AsyncSession, 
    player: Player, 
):

    query = select([Bet.numbers, func.sum(Bet.amount).label("amount")]) \
        .where(and_(
                    Bet.player_id == player.id,
                    Bet.chat_id == message.chat.id
        )) \
        .group_by(Bet.chat_id, Bet.numbers)

    bets = (await session.execute(query)).all()
    
    res = i18n.t('commands.bets.label')
    for bet in bets:
        numbers, amount = bet
        res += i18n.t('commands.bets', {"amount": f"{amount:,}", "numbers": numbers}, amount=amount)

    await message.reply(res)
    await analytics.action(message.chat.id, EventAction.SEND_MESSAGE)
    

def register(dp: Dispatcher):
    dp.register_message_handler(show_bets, Command('ставки', prefixes='!'))
