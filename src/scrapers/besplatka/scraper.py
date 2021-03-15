from typing import List

from src.core.config import scrapers_settings
from src.db.models import Flat
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
            downloader=downloader
        )
        self._parser = BesplatkaParse()

    async def scrape(self) -> List[Flat]:
        response = await self._downloader.get(url=self.listing_url, params=self.REQUEST_PARAMS)
        await self.check_response(response)
        flats = []
        parsed_flats = self._parser.parse_listing(
            content=response.text,
            url=str(response.url)
        )
        flats.extend(parsed_flats)

        while next_page_url := self._parser.parse_next_page_url(content=response.text, url=str(response.url)):
            parsed_flats = self._parser.parse_listing(
                content=response.text,
                url=str(response.url)
            )
            flats.extend(parsed_flats)

            response = await self._downloader.get(url=next_page_url)
            await self.check_response(response)

        return flats
