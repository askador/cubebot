import asyncio

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.data.config import config
from bot.db.base import create_pool
from bot.analytics import analytics
from bot.utils import logging, set_bot_commands, redis_storage, get_allowed_updates_list, on_shutdown
from bot import middlewares, filters, handlers


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
    reset_color = "\033[0;0m"
    logger.info(f"Starting bot {green}https://t.me/{(await bot.me).username}{reset_color}")

    try:
        await dp.skip_updates()
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.send_message(config.bot.issue_chat, "Bot started!")
        await dp.start_polling(allowed_updates=get_allowed_updates_list(dp))
    finally:
        logger.warning("Stopping bot")
        await on_shutdown(dp, db_pool, config)
        await redis_storage.close()



if __name__ == '__main__':
    task = None
    try:
        task = asyncio.run(main()) 
    except KeyboardInterrupt:
        if task:
            task.cancel()