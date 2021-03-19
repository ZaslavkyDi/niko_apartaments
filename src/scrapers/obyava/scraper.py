from src.core.config import scrapers_settings
from src.scrapers.base_scraper import BaseScraper
from src.scrapers.obyava.parser import ObyavaParse
from src.scrapers.rieltor.parser import RieltorParse
from src.scrapers.utils.downloader import AsyncDownloader


class ObyavaScraper(BaseScraper[RieltorParse]):
    REQUEST_PARAMS = {
        'price_max': scrapers_settings.max_flat_price
    }

    def __init__(self, downloader: AsyncDownloader):
        super().__init__(
            listing_url=scrapers_settings.obyava_listing_url,
            downloader=downloader,
            parser=ObyavaParse()
        )
