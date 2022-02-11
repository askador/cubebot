from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from sqlalchemy import delete, func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Player, Bet
from bot.types.Localization import I18nJSON
from bot.utils import rate_limit


@rate_limit()
async def cancel_bets(
    message: types.Message, 
    i18n: I18nJSON, 
    session: AsyncSession, 
    player: Player, 
):
    query = select([func.sum(Bet.amount).label("amount")]) \
        .where(and_(
            Bet.chat_id == message.chat.id,
            Bet.player_id == player.id
        )) \
        .group_by(Bet.player_id, Bet.chat_id)

    money = (await session.execute(query)).fetchone()
    
    if money:
        player.money += money[0]

        await session.execute(delete(Bet)\
            .where(and_(
                Bet.chat_id == message.chat.id,
                Bet.player_id == player.id
        )))

        await session.commit()

    await message.reply(i18n.t("commands.cancel_bets"))

def register(dp: Dispatcher):
    dp.register_message_handler(cancel_bets, Command('отмена', prefixes='!'))