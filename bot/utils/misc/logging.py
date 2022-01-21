import logging

from pathlib import Path
from loguru import logger

from bot.data.config import Logging


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR:    "ERROR",
        logging.WARNING:  "WARNING",
        logging.INFO:     "INFO",
        logging.DEBUG:    "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


def setup_logger(config: Logging):
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.getLevelName(config.level))
    for ignore in config.ignored:
        logger.disable(ignore)
    if config.path:
        logger.add(Path.joinpath(config.path, "{time}.log"))
    logger.info("Logging is successfully configured")
