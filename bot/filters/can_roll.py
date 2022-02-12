from typing import Optional, Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from loguru import logger

from sqlalchemy import and_, select, func

from bot.db.models import Game, Bet


class CanRoll(BoundFilter):
    async def check(self, message: types.Message) -> Union[bool, "dict[str, bool]"]:
        data = ctx_data.get()
        session = data.get('session')
        
        game: Optional[tuple[Game]] = (await session.execute(
            select(Game)
            .where(Game.chat_id == message.chat.id)
        )).fetchone()

        if not game or game[0].is_rolling:
            return False

        player_has_bets = (await session.execute(
            select(func.count(Bet.id))
            .where(and_(
                Bet.player_id == message.from_user.id, 
                Bet.chat_id == message.chat.id
            ))
        )).fetchone()

        if player_has_bets[0] == 0:
            return {"no_bets": True}

        return True
