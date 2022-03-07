from aiogram import Dispatcher, types
from aiogram.types.message import ContentType

from bot.db.models import Chat
from bot.analytics import analytics
from bot.analytics.events import EventUpdateType

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


async def chat_migration(message: types.Message, session: AsyncSession) -> None:
    old_chat_id = message.chat.id
    new_chat_id = message.migrate_to_chat_id

    await analytics.update(None, new_chat_id, EventUpdateType.CHAT_MIGRATION)

    await session.execute(
        update(Chat)
        .where(Chat.id == old_chat_id)
        .values({"id": new_chat_id}) 
    )

    await session.commit()


def register(dp: Dispatcher):
    dp.register_message_handler(
        chat_migration, 
        content_types=[ContentType.MIGRATE_FROM_CHAT_ID, ContentType.MIGRATE_TO_CHAT_ID]
    )
