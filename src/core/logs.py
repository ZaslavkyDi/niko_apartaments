import sys

from loguru import logger

from src.core.config import app_settings

LOG_LEVEL = 'DEBUG'
LOG_FILE_PATH = '../logs/file_{time}.log'


def init_logger() -> None:
    logger.remove()
    logger.add(sys.stdout, level=LOG_LEVEL)

    if not app_settings.debug:
        logger.add(LOG_FILE_PATH, level=LOG_LEVEL, rotation='50 MB')
