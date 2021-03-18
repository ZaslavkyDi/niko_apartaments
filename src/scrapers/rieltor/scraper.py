from src.core.config import scrapers_settings
from src.scrapers.base_scraper import BaseScraper
from src.scrapers.rialtor.parser import RealtorParse
from src.scrapers.utils.downloader import AsyncDownloader


class RealtorScraper(BaseScraper[RealtorParse]):
    REQUEST_PARAMS = {
        'price_max': scrapers_settings.max_flat_price
    }

    def __init__(self, downloader: AsyncDownloader):
        super().__init__(
            listing_url=scrapers_settings.realtor_listing_url,
            downloader=downloader,
            parser=RealtorParse()
        )
