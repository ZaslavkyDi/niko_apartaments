from asyncio import sleep
from typing import Dict

from loguru import logger
from tortoise.exceptions import IntegrityError

from src.core.enums import ScrapersEnum
from src.db.models import Flat
from src.scrapers.base_scraper import BaseScraper
from src.scrapers.besplatka.scraper import BesplatkaScraper
from src.scrapers.utils.downloader import AsyncDownloader


class ScraperExecutor:

    def __init__(self):
        downloader = AsyncDownloader()
        self._scrapers = self._init_scrapers(downloader)

    async def run_scraping(self) -> None:
        while True:
            for scraper in list(ScrapersEnum):
                await self._scrape_and_save(scraper_name=scraper)
                await sleep(10)

    async def _scrape_and_save(self, scraper_name: ScrapersEnum) -> None:
        logger.info(f'Start {scraper_name.besplatka}!')
        try:
            scraper = self._scrapers[scraper_name]
            scraped_flats = await scraper.scrape()
            [await self._save_flat_silently(flat) for flat in scraped_flats]

        except KeyError:
            pass

        logger.info(f'Start {scraper_name.besplatka}!')

    @staticmethod
    def _init_scrapers(downloader: AsyncDownloader, **kwargs) -> Dict[ScrapersEnum, BaseScraper]:
        return {
            ScrapersEnum.besplatka: BesplatkaScraper(downloader=downloader),
        }

    @staticmethod
    async def _save_flat_silently(flat: Flat) -> None:
        try:
            await flat.save()
        except IntegrityError:
            pass
