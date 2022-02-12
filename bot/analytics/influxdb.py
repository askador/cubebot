from aioinflux import InfluxDBClient
from loguru import logger
from bot.data.config import config

# influx = InfluxDBClient(
#     host=config.influxdb.host, 
#     database=config.influxdb.database,
#     username=config.influxdb.username, 
#     password=config.influxdb.password
# )

async def check():
    logger.info(f"Checking influxdb connection")
    # await influx.ping()
