import asyncio

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.data.config import config
from bot.db.base import create_pool
from bot.analytics import analytics
from bot.utils import logging, set_bot_commands, redis_storage, get_allowed_updates_list
from bot import middlewares, filters, handlers
from bot.utils import on_shutdown


async def main():
    # Setting up logger
    logging.setup_logger(config.logging)

    # fsm storage 
    if config.bot.fsm_type == "redis":
        storage = RedisStorage2(
            host=config.redis.host,
            port=config.redis.port,
            password=config.redis.password,
            db=config.redis.db
        )
    else:
        storage = MemoryStorage()

    # Checking influxb connection
    await analytics.create_client()
    await analytics.ping()

    # Creating bot and its dispatcher
    bot = Bot(token=config.bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)

    # Setting up database pool
    db_pool = await create_pool(config.db)
    is_dev = True if config.project_phase == 'dev' else False
    
    middlewares.setup(dp, config.i18n, db_pool, is_dev)
    filters.setup(dp)
    handlers.setup(dp)

    # Register /-commands in UI
    await set_bot_commands(bot)
    
    green = "\033[92m"
    logger.info(f"Starting bot {green}https://t.me/{(await bot.me).username}")

    try:
        await dp.skip_updates()
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(allowed_updates=get_allowed_updates_list(dp))
    finally:
        # await on_shutdown(dp)
        logger.warning("Stopping bot")
        await dp.storage.close()
        await dp.storage.wait_closed()
        await redis_storage.close()
        await on_shutdown.close_all_games(dp, db_pool, config.i18n)
        await bot.send_message(-1001534253038, "Bot stopped!")
        session = await bot.get_session()
        await session.close() # type: ignore


if __name__ == '__main__':
    task = None
    try:
        task = asyncio.run(main()) 
    except KeyboardInterrupt:
        if task:
            task.cancel()