import asyncio

from src.core.logs import init_logger
from src.db.database import init_db
from src.scrapers.executor import ScraperExecutor


async def run_app() -> None:
    init_logger()
    await init_db()

    scraper_executor = ScraperExecutor()
    await scraper_executor.run_scraping()


if __name__ == '__main__':
    asyncio.run(run_app())
