import sys
from loguru import logger

from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from bot.data.config import DB

Base = declarative_base()

async def create_pool(db: DB):
    logger.info("Establishing database pool")

    connection_uri = f"postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}"
    engine = create_async_engine(url=make_url(connection_uri))
    pool: sessionmaker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

    try:
        async with pool() as pool:
            await pool.execute("SELECT 1+1 AS RESULT") # type: ignore
    except Exception as e:
        logger.exception(e)
        sys.exit()

    return pool

"""
Exceptions:
 user       - asyncpg.exceptions.InvalidPasswordError: password authentication failed for user "ostgres"
 password   - asyncpg.exceptions.InvalidPasswordError: password authentication failed for user "postgres"
 db_name    - asyncpg.exceptions.InvalidCatalogNameError: database "ubebot" does not exist
 host       - socket.gaierror: [Errno 11001] getaddrinfo failed
 port       - ectionRefusedError: [WinError 1225] The remote computer refused the network connection
"""