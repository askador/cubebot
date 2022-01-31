from aiogram.types import User, CallbackQuery, Message
from aiogram.dispatcher.middlewares import BaseMiddleware

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Player


class ACLMiddleware(BaseMiddleware):
    async def setup_player(self, data: dict, user: User):
        player_id = user.id
    
        session: AsyncSession = data["session"]

        player: Player = await session.merge(Player(id=player_id, fullname=user.full_name))
        await session.commit()

        data["player"] = player

    async def on_process_message(self, message: Message, data: dict):
        await self.setup_player(data, message.from_user)

    async def on_process_callback_query(self, query: CallbackQuery, data: dict):
        await self.setup_player(data, query.from_user)