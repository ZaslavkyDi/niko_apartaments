from typing import List

from src.core.config import scrapers_settings
from src.db.models import Flat
from src.scrapers.base_scraper import BaseScraper
from src.scrapers.domria.parser import DomriaParse
from src.scrapers.utils.downloader import AsyncDownloader


class DomriaScraper(BaseScraper[DomriaParse]):
    REQUEST_PARAMS = {
        'links-under-filter': 'on',
        'category': 1,
        'realty_type': 2,
        'operation_type': 3,
        'fullCategoryOperation': '1_2_3',
        'page': 0,
        'state_id': 19,
        'city_id': 19,
        'limit': 10000,
        'sort': 'inspected_sort',
        'period': 0,
        'ch': f'235_t_{scrapers_settings.max_flat_price},246_244'
    }
    FLAT_INFO_URL_TEMPLATE = 'https://dom.ria.com/node/searchEngine/v2/view/realty/{id}'

    def __init__(self, downloader: AsyncDownloader):
        super().__init__(
            listing_url=scrapers_settings.domria_listing_url,
            downloader=downloader,
            parser=DomriaParse()
        )

    async def scrape(self) -> List[Flat]:
        flats_ids = await self._scrape_flats_ids()

        flats = []
        for flat_id in flats_ids:
            flat_url = self.FLAT_INFO_URL_TEMPLATE.format(id=flat_id)
            response = await self._downloader.get(url=flat_url)
            await self.check_response(response)

            flat_json = response.json()
            flat = self._parser.parse_flat(content=flat_json)
            flats.append(flat)

        return [i for i in flats if i]

    async def _scrape_flats_ids(self) -> List[int]:
        response = await self._downloader.get(url=self.listing_url, params=self.REQUEST_PARAMS)
        await self.check_response(response)

        listing_json = response.json()
        return listing_json['items']
