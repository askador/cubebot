# -*- coding: utf-8 -*-
import asyncio

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.data.config import config
from bot.db.base import create_pool
from bot.utils.misc import logging
from bot.utils import set_bot_commands
from bot import middlewares, filters, handlers


async def main():
    # Reading config file

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
    
    green = "\033[92m"
    logger.info("Starting bot " \
                f"{green}https://t.me/{(await bot.me).username}"
    )

    try:
        await dp.reset_webhook()
        await dp.skip_updates()
        await dp.start_polling()
    finally:
        logger.warning("Stopping bot")
        await dp.storage.close()
        await dp.storage.wait_closed()
        # await bot.send_message(526497876, "Bot stopped!")
        session = await bot.get_session()
        await session.close() # type: ignore


if __name__ == '__main__':
    asyncio.run(main()) 
