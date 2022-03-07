from typing import Optional, Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from loguru import logger

from sqlalchemy import and_, select, func

from bot.db.models import Game, Bet


class CanRoll(BoundFilter):
    async def check(self, event: Union[types.Message, types.CallbackQuery]) -> Union[bool, "dict[str, bool]"]:
        data = ctx_data.get()
        session = data.get('session')

        if isinstance(event, types.CallbackQuery):
            chat_id = event.message.chat.id
            user_id = event.from_user.id
        else:
            chat_id = event.chat.id
            user_id = event.from_user.id
        
        game: Optional[tuple[Game]] = (await session.execute(
            select(Game)
            .where(Game.chat_id == chat_id)
        )).fetchone()

        if not game or game[0].is_rolling:
            return False

        player_has_bets = (await session.execute(
            select(func.count(Bet.id))
            .where(and_(
                Bet.player_id == user_id, 
                Bet.chat_id == chat_id
            ))
        )).fetchone()

        if player_has_bets[0] == 0:
            return {"no_bets": True}

        return True
