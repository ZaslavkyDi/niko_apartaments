import asyncio

from loguru import logger

from src.core.config import app_settings
from src.core.logs import init_logger
from src.db.database import init_db
from src.scrapers.executor import ScraperExecutor


async def run_app() -> None:
    init_logger()
    await init_db()

    scraper_executor = ScraperExecutor()
    await scraper_executor.run_scraping()


if __name__ == '__main__':
    logger.info(f'DB: URL {app_settings.db_url}')
    asyncio.run(run_app())
