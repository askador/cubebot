from typing import Optional

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Player, Game, Bet
from bot.filters import IsBet
from bot.types.Localization import I18nJSON
from bot.utils import rate_limit


@rate_limit(key="bet")
async def bet(
    message: types.Message, 
    i18n: I18nJSON, 
    session: AsyncSession, 
    player: Player, 
    bet_data: "dict[str, int]"
):

    chat_id = message.chat.id

    game: tuple[Optional[Game]] = (await session.execute(
        select(Game)
        .where(Game.chat_id == chat_id)
    )).fetchone()

    if not game or game[0].is_rolling:                              # type: ignore
        return 

    if not player.money >= bet_data.get("amount", float('inf')):
        return await message.reply(i18n.t('money.not_enough')) 

    await session.execute(
        update(Player)
        .where(Player.id == player.id)
        .values({"money": player.money - bet_data.get("amount")})   # type: ignore
    )

    session.add(Bet(
        player_id=player.id,
        chat_id=chat_id,
        amount=bet_data.get("amount"),
        numbers=bet_data.get("numbers")
    ))
    await session.commit()

    await message.answer(i18n.t(
        'commands.bet', 
        {
            "id": player.id,
            "name": player.fullname,
            "amount": f"{bet_data.get('amount'):,}",
            "numbers": bet_data.get("numbers")   
        },
        amount = bet_data.get('amount')
    ))


def register(dp: Dispatcher):
    dp.register_message_handler(bet, Command(['ставка', 'с'], prefixes='!'), IsBet())