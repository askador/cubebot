from typing import Optional, Union
from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Bet, Game, Player
from bot.types.Localization import I18nJSON

cd = CallbackData('game', 'action', 'amount', 'number')

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

    game: tuple[Optional[Game]] = (await session.execute(
        select(Game)
        .where(Game.chat_id == chat_id)
    )).fetchone()

    if not game[0] or game[0].is_rolling: 
        return 

    if not player.money >= amount:
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

    await cb.answer()

def register(dp: Dispatcher):
    dp.register_callback_query_handler(bet, cd.filter(action='bet'))