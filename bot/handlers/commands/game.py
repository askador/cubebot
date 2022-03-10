from contextlib import suppress

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import ChatNotFound

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Game
from bot.filters import StrictCommand
from bot.analytics import analytics
from bot.analytics.events import EventAction, EventCommand
from bot.types.Localization import I18nJSON
from bot.keyboards.inline import new_game_kb
from bot.utils.throttling import rate_limit

@rate_limit()
@analytics.command(EventCommand.GAME)
async def new_game(message: types.Message, i18n: I18nJSON, session: AsyncSession):
    chat_id = message.chat.id

    game = (await session.execute(
        select(Game)
        .where(Game.chat_id == chat_id)
    )).fetchone()
    
    if game:
        await analytics.action(chat_id, EventAction.SEND_MESSAGE)
        return await message.answer(i18n.t('commands.game.already_exists'))

    session.add(Game(chat_id=chat_id))
    await session.commit()

    await message.answer(i18n.t('commands.game.message'), reply_markup=new_game_kb(i18n.language_key))
    await analytics.action(chat_id, EventAction.SEND_MESSAGE)


def register(dp: Dispatcher):
    dp.register_message_handler(new_game, Command('game'), StrictCommand())
