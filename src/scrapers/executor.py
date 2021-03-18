from asyncio import sleep
from typing import Dict

from loguru import logger
from tortoise.exceptions import IntegrityError

from src.core.config import scrapers_settings
from src.core.enums import ScrapersEnum
from src.db.models import Flat
from src.scrapers.base_scraper import BaseScraper
from src.scrapers.besplatka.scraper import BesplatkaScraper
from src.scrapers.domria.scraper import DomriaScraper
from src.scrapers.rieltor.scraper import RieltorScraper
from src.scrapers.utils.downloader import AsyncDownloader


class ScraperExecutor:

    def __init__(self):
        downloader = AsyncDownloader()
        self._scrapers = self._init_scrapers(downloader)

    async def run_scraping(self) -> None:
        while True:
            for scraper in list(ScrapersEnum):
                await self._run_scraper(scraper)

    @logger.catch
    async def _run_scraper(self, scraper: ScrapersEnum) -> None:
        try:
            await self._scrape_and_save(scraper_name=scraper)
            await sleep(scrapers_settings.scraper_sleep_seconds)
        except Exception as e:
            logger.error(e)

    async def _scrape_and_save(self, scraper_name: ScrapersEnum) -> None:
        logger.info(f'Start {scraper_name}!')

        scraper = self._scrapers[scraper_name]
        scraped_flats = await scraper.scrape()
        [await self._save_flat_silently(flat) for flat in scraped_flats]

        logger.info(f'End {scraper_name}!')

    @staticmethod
    def _init_scrapers(downloader: AsyncDownloader, **kwargs) -> Dict[ScrapersEnum, BaseScraper]:
        return {
            ScrapersEnum.besplatka: BesplatkaScraper(downloader=downloader),
            ScrapersEnum.domria: DomriaScraper(downloader=downloader),
            ScrapersEnum.rieltor: RieltorScraper(downloader=downloader),
        }

    @staticmethod
    async def _save_flat_silently(flat: Flat) -> None:
        try:
            await flat.save()
        except IntegrityError:
            pass
