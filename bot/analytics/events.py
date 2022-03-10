from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Union


class EventUpdateType(Enum):
    UPDATE = 'update'
    ERROR = 'error'
    MESSAGE = 'message'
    CALLBACK_QUERY = 'callback_query'
    CHAT_MIGRATION = 'chat_migration'


class EventAction(Enum):
    SEND_MESSAGE = 'send_message'
    CALLBACK_QUERY_ANSWER = 'callback_query_answer'


class EventCommand(Enum):
    PING = '/ping'
    START = '/start'
    HELP = '/help'
    GAME = '/game'
    ISSUE = '/issue'
    MONEY = '/money'
    PROFILE = '/profile'
    ROLL = '/roll'
    LOGS = '/logs'
    GIVE_MONEY = '!передать'
    CANCEL_BETS = '!отмена'
    BET = '!ставка'
    SHOW_BETS = '!ставки'

class EventCbQueryAction(Enum):
    ROLL = 'roll'
    BET = 'bet'
    BONUS = 'bonus'
    GIVEAWAY = 'giveaway'



Events = Union[EventCommand, EventUpdateType, EventAction, EventCbQueryAction, str]


@dataclass
class Event:
    timestamp: datetime
    user_id: Optional[Union[int, str]]
    chat_id: Optional[Union[int, str]]
    event: Events


