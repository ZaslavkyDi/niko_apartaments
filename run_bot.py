import asyncio

from loguru import logger

from src.bot.bot import run_bot
from src.core.config import app_settings
from src.core.logs import init_logger
from src.db.database import init_db


async def run_app() -> None:
    init_logger()
    await init_db()
    await run_bot()


if __name__ == '__main__':
    logger.info(f'DB: URL {app_settings.db_url}')
    asyncio.run(run_app())
