from abc import ABC
from typing import List, Union, Generic, TypeVar, Dict

from httpx import Response
from loguru import logger

from src.db.models import Flat
from src.scrapers.utils.downloader import AsyncDownloader

Parser = TypeVar('Parser')


class BaseScraper(ABC, Generic[Parser]):
    REQUEST_PARAMS: Dict = {}

    def __init__(self, listing_url: str, downloader: AsyncDownloader, parser: Parser):
        self._listing_url = listing_url
        self._downloader = downloader
        self._parser = parser

    @property
    def listing_url(self) -> str:
        return self._listing_url

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

    @staticmethod
    async def check_response(
            response: Response,
            available_statuses: Union[int, List[int]] = 200
    ) -> None:
        if isinstance(available_statuses, int):
            available_statuses = [available_statuses]

        if response.status_code not in available_statuses:
            error_message = f'Not valid status code [url={response.url}, status_code={response.status_code}]! Expected: {available_statuses}'
            logger.error(error_message)
            raise ValueError(error_message)
