from typing import Optional, Dict
from urllib.parse import urljoin

from loguru import logger

from src.db.models import Flat


class DomriaParse:
    URL_DOMAIN = 'https://dom.ria.com'
    URL_DOMAIN_PART = 'uk'

    @logger.catch
    def parse_flat(self, content: Dict) -> Optional[Flat]:
        url = self._parse_url(content)
        price = content.get('price')

        if not price:
            return None

        return Flat(
            url=url,
            price=price
        )

    @logger.catch()
    def _parse_url(self, content: Dict) -> str:
        flat_url_path = f"{self.URL_DOMAIN_PART}/{content['beautiful_url']}".replace('//', '/')
        url = urljoin(self.URL_DOMAIN, flat_url_path)
        return url
