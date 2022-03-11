import asyncio

from pathlib import Path

from aiogram import Bot, Dispatcher
from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, select, update
from bot.data.config import Config, I18nConfig

from bot.db.models import Game
from bot.analytics import analytics
from bot.analytics.events import EventAction
from bot.types.Localization import I18nJSON
from bot.handlers.commands.roll import process_bets


async def close_all_games(dp: Dispatcher, db_pool: sessionmaker, i18n_config: I18nConfig):
    logger.warning("Stopping all active games")
    session: AsyncSession = db_pool()
    bot: Bot = dp.bot
    i18n = I18nJSON(i18n_config)
    i18n.set_language('ru')

    games: list[Game] = (await session.execute(select(Game))).scalars().all()

    for game in games:
        await session.execute(update(Game).where(Game.chat_id == game.chat_id).values({"is_rolling": True}))
        await session.commit()

        dice_msg = await bot.send_dice(game.chat_id, emoji="🎲")
        await analytics.action(game.chat_id, EventAction.SEND_MESSAGE)
        number = dice_msg.dice.value

        results = f'🎲  {number}\n'
        results += await process_bets(number, game.chat_id, session, i18n)

        await asyncio.sleep(4)
        await bot.send_message(game.chat_id, results)
        await analytics.action(game.chat_id, EventAction.SEND_MESSAGE)

    await session.close()


async def send_logs(dp: Dispatcher, issue_chat: str):
    logs_dir = Path(__file__).parents[2].joinpath(f'logs_{(await dp.bot.get_me()).username}')
    log_files = logs_dir.glob('*.log')
    latest_log = max(log_files, key=Path.stat)
    with open(latest_log, 'r') as file:
        await dp.bot.send_document(issue_chat, file)
    

async def on_shutdown(dp: Dispatcher, db_pool: sessionmaker, config: Config):
    await close_all_games(dp, db_pool, config.i18n)
    await send_logs(dp, config.bot.issue_chat)
    await dp.storage.close()
    await dp.storage.wait_closed()
    session = await dp.bot.get_session()
    await session.close() # type: ignore
    await dp.bot.send_message(config.bot.issue_chat, "Bot stopped!")
