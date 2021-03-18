from src.core.config import scrapers_settings
from src.scrapers.base_scraper import BaseScraper
from src.scrapers.besplatka.parser import BesplatkaParse
from src.scrapers.utils.downloader import AsyncDownloader


class BesplatkaScraper(BaseScraper):
    REQUEST_PARAMS = {
        'prop[136][to]': scrapers_settings.max_flat_price,
        'currency': 'UAH',
    }

    def __init__(self, downloader: AsyncDownloader):
        super().__init__(
            listing_url=scrapers_settings.besplatka_listing_url,
            downloader=downloader,
            parser=BesplatkaParse()
        )
