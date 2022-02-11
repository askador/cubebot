from enum import Enum
from influxdb import InfluxDBClient
from datetime import datetime


class DBParams:
    STATS_DB   = None
    STATS_HOST = None
    STATS_USER = None
    STATS_PASS = None


class EventCommand(Enum):
    START = "/start"
    RESTART = "/restart"
    STOP = "/stop"
    PING = "/ping"
    HELP = "/help"


async def log(user_id: int, event: EventCommand):
    data = [{
        "measurement": "bot_commands",
        "time": datetime.utcnow(),
        "fields": {"event": 1},
        "tags": {
            "user": str(user_id),
            "command": event.value
        }
    }]
    # client = InfluxDBClient(host=DBParams.STATS_HOST, database=DBParams.STATS_DB,
    #                         username=DBParams.STATS_USER, password=DBParams.STATS_PASS)
    # client.write_points(data)
