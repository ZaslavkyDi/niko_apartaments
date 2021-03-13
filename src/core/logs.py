import sys

from loguru import logger

LOG_LEVEL = 'DEBUG'
LOG_FILE_PATH = 'logs/file_{time}.log'


def init_logger() -> None:
    logger.remove()
    logger.add(sys.stdout, level=LOG_LEVEL)
    logger.add(LOG_FILE_PATH, level=LOG_LEVEL, rotation='50 MB')
