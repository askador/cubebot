from aiogram.types import User, CallbackQuery, Message, Chat as TGChat
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Player, Chat


class ACLMiddleware(BaseMiddleware):
    async def setup_data(self, data: dict, user: User, chat: TGChat) -> None:
        player_id = user.id
        chat_id = chat.id
    
        session: AsyncSession = data["session"]

        await session.merge(Player(id=player_id, fullname=user.full_name))
        await session.merge(Chat(id=chat_id))
        await session.commit()
        player: Player = await session.get(Player, player_id)

        data["player"] = player
        

    async def on_process_message(self, message: Message, data: dict):
        await self.setup_data(data, message.from_user, message.chat)

    async def on_process_callback_query(self, query: CallbackQuery, data: dict):
        await self.setup_data(data, query.from_user, query.message.chat)
