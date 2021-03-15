from typing import Optional, Dict
from urllib.parse import urljoin

from loguru import logger

from src.db.models import Flat


class DomriaParse:

    @logger.catch
    def parse_flat(self, content: Dict, url: str) -> Optional[Flat]:
        url = urljoin(url, content['beautiful_url'])
        price = content.get('price')

        if price:
            return Flat(
                url=url,
                price=price
            )
