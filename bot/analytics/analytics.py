import inspect

from datetime import datetime
from typing import Callable, Union
from loguru import logger

from aioinflux import InfluxDBClient

from aiogram.types import Message, CallbackQuery

from bot.analytics.events import (
    Event, EventAction, EventCommand, EventUpdateType, EventCbQueryAction,
)
from bot.data.config import config, InfluxDBConfig


def _get_spec(func: Callable):
    while hasattr(func, '__wrapped__'):  # Try to resolve decorated callbacks
        func = func.__wrapped__
    return inspect.getfullargspec(func)


def _check_spec(spec: inspect.FullArgSpec, kwargs: dict):
    if spec.varkw:
        return kwargs

    return {k: v for k, v in kwargs.items() if k in set(spec.args + spec.kwonlyargs)}


class Analytics:
    
    def __init__(self, config: InfluxDBConfig) -> None:
        self.config = config

    async def create_client(self):
        self.client = InfluxDBClient(
            host=self.config.host, 
            port=self.config.port,
            database=self.config.database,
            username=self.config.username, 
            password=self.config.password
        )

    async def ping(self):
        if not self.client:
            logger.error("InfluxDBClient must be created\nuse `await analytics.create_client()`")
            return
        ping = await self.client.ping()
        logger.info(f"InfluxDB PING: {ping.get('X-Influxdb-Version')}")

    async def write(self, measurement: str, event: Event):
        event_name = event.event if isinstance(event.event, str) else event.event.value 

        data = {
            "measurement": measurement,
            "time": event.timestamp,
            "fields": {"value": 1},
            "tags": {
                "event": event_name
            }
        }

        if event.chat_id:
            data['tags'].update({"chat_id": str(event.chat_id)})
        if event.user_id:
            data['tags'].update({"user_id": str(event.user_id)})

        await self.client.write([data])

    def command(self, command: EventCommand):
        """Decorator for command handler"""

        def decorator(func):
            spec = _get_spec(func)
            async def wrapper(message: Message, *args, **kwargs):
                partial_data = _check_spec(spec, kwargs)
                user_id = message.from_user.id
                chat_id = message.chat.id

                await self.write("commands", Event(
                    timestamp=datetime.utcnow(),
                    user_id=user_id,
                    chat_id=chat_id, 
                    event=command
                ))

                return await func(message, *args, **partial_data)
            return wrapper
        return decorator

    def cb_query(self, query: EventCbQueryAction):
        """Decorator for callback query handler handler"""

        def decorator(func):
            spec = _get_spec(func)
            async def wrapper(cb: CallbackQuery, *args, **kwargs):
                partial_data = _check_spec(spec, kwargs)
                user_id = cb.from_user.id
                chat_id = cb.message.chat.id

                await self.write("callback_queries", Event(
                    timestamp=datetime.utcnow(),
                    user_id=user_id,
                    chat_id=chat_id, 
                    event=query
                ))

                return await func(cb, *args, **partial_data)
            return wrapper
        return decorator

    async def action(self, chat_id, action: EventAction):
        """
        Metrics of bot actions 
        """

        await self.write("actions", Event(
            timestamp=datetime.utcnow(),
            user_id=None,
            chat_id=chat_id, 
            event=action
        ))

    async def update(self, user_id, chat_id, update: EventUpdateType):
        """
        Metrics of update events
        """

        await self.write("updates", Event(
            timestamp=datetime.utcnow(),
            user_id=user_id,
            chat_id=chat_id, 
            event=update
        ))
        

analytics = Analytics(config.influxdb)
