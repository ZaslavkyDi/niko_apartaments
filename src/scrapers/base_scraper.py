from abc import ABC, abstractmethod
from typing import List, Union

from httpx import Response
from loguru import logger

from src.db.models import Flat
from src.scrapers.utils.downloader import AsyncDownloader


class BaseScraper(ABC):

    def __init__(self, listing_url: str, downloader: AsyncDownloader):
        self._listing_url = listing_url
        self._downloader = downloader

    @property
    def listing_url(self) -> str:
        return self._listing_url

    @abstractmethod
    async def scrape(self) -> List[Flat]:
        pass

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
