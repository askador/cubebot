import asyncio

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.data.config import Config, load_config
from bot.db.base import create_pool
from bot.utils.misc import logging
from bot.utils import set_bot_commands
from bot import middlewares
from bot import filters
from bot import handlers


async def main():
    # Reading config file
    config: Config = load_config()

    # Setting up logger
    logging.setup_logger(config.logging)

    # c fsm storage 
    if config.bot.fsm_type == "redis":
        storage = RedisStorage2(
            host=config.redis.host,
            port=config.redis.port,
            password=config.redis.password,
            db=config.redis.db
        )
    else:
        storage = MemoryStorage()


    # Creating bot and its dispatcher
    bot = Bot(token=config.bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)

    # Setting up database pool
    db_pool = await create_pool(config.db)

    middlewares.setup(dp, config.middlewares, db_pool)
    filters.setup(dp)
    handlers.setup(dp)

    # Register /-commands in UI
    await set_bot_commands(bot)

    logger.info("Starting bot")

    try:
        await dp.reset_webhook()
        await dp.start_polling()
    finally:
        await asyncio.sleep(1)
        logger.info("Stopping bot")
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.get_session().close() # type: ignore the line.


if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
        loop.close()
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
