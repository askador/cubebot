import json
from loguru import logger
from typing import Any, Optional, Union

from aioredis import Redis, ConnectionPool

from bot.data.config import RedisConfig, config


class RedisDataStorage:
    def __init__(self, config: RedisConfig) -> None:
        url = f"redis://default:{config.password}@{config.host}:{config.port}"
        connection_kwargs = {"decode_responses": True, "db": config.db}
        pool = ConnectionPool.from_url(url, **connection_kwargs)
        self.redis: Redis = Redis(connection_pool=pool)

    async def close(self) -> None:
        await self.redis.close()

    def build_key(self, prefix, chat, user) -> str:
        if chat is None and user is None:
            raise ValueError(
                '`user` or `chat` parameter is required but no one is provided!')
        if user is None:
            user = chat
        elif chat is None:
            chat = user

        prefix = prefix if prefix is not None else "data"
        return ":".join(tuple(map(str, [prefix, chat, user])))

    async def set(
        self,
        *,
        prefix: str = None,
        user: Union[int, str, None] = None,
        chat: Union[int, str, None] = None,
        data: Union[str, "dict[str, Any]"] = None,
        ttl: Optional[int] = None
    ) -> None:
        redis_key = self.build_key(prefix, chat, user)
        if not data:
            await self.redis.delete(redis_key)
            return

        if isinstance(data, dict):
            data = json.dumps(data)
        await self.redis.set(redis_key, data, ex=ttl)

    async def get(
        self,
        prefix: str = None,
        user: Union[int, str, None] = None,
        chat: Union[int, str, None] = None
    ) -> Union[str, "dict[str, Any]"]:
        redis_key = self.build_key(prefix, user, chat)
        value = await self.redis.get(redis_key)
        if value is None:
            return {}
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        if value[0] != '{':
            return value
        return json.loads(value)


redis_storage = RedisDataStorage(config.redis)

