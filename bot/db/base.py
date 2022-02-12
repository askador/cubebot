from loguru import logger
from sys import exit
from socket import gaierror
from asyncpg.exceptions import InvalidPasswordError, InvalidCatalogNameError

from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from bot.data.config import Database

Base = declarative_base()

async def create_pool(db: Database) -> sessionmaker:
    logger.info("Establishing database pool")

    connection_uri = f"postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}"
    engine = create_async_engine(connection_uri, echo=False)
    
    try:
        async with engine.begin() as conn:
            # initialize all tables
            await conn.run_sync(Base.metadata.create_all)
            # await conn.run_sync(text("SELECT 1+1 AS RESULT"))
    except gaierror as addrexc:
        logger.exception("host is invalid", addrexc)
        exit()
    except InvalidPasswordError as e:
        logger.exception(e)
        exit()
    except InvalidCatalogNameError as e:
        logger.exception(e)
        exit()
    except ConnectionRefusedError as e:
        logger.exception("port is invalid", e)
        exit()

    pool: sessionmaker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

    return pool

"""
Exceptions:
 user       - asyncpg.exceptions.InvalidPasswordError: password authentication failed for user "ostgres"
 password   - asyncpg.exceptions.InvalidPasswordError: password authentication failed for user "postgres"
 db_name    - asyncpg.exceptions.InvalidCatalogNameError: database "ubebot" does not exist
 host       - socket.gaierror: [Errno 11001] getaddrinfo failed
 port       - ConnectionRefusedError: [WinError 1225] The remote computer refused the network connection
"""
