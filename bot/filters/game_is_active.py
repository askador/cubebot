from typing import Optional, Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from loguru import logger

from sqlalchemy import and_, select, func

from bot.db.models import Game, Bet


class GameIsActive(BoundFilter):
    async def check(self, event: Union[types.Message, types.CallbackQuery]) -> bool:
        data = ctx_data.get()
        session = data.get('session')

        if isinstance(event, types.CallbackQuery):
            chat_id = event.message.chat.id
        else:
            chat_id = event.chat.id

        game: tuple[Optional[Game]] = (await session.execute(
            select(Game)
            .where(Game.chat_id == chat_id)
        )).fetchone()

        if not game or game[0].is_rolling:                              # type: ignore
            return False

        return True