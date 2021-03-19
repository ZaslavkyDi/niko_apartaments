from typing import Optional, List
from urllib.parse import urljoin

from loguru import logger
from parsel import Selector

from src.core.config import scrapers_settings
from src.db.models import Flat


class ObyavaParse:
    NEXT_PAGE_URL_XPATH = '//li[@class="next"]/a/@href'
    FLAT_ITEM_XPATH = '//div[@class="classified-item"]'
    FLAT_URL_XPATH = './/h2/a/@href'
    FLAT_PRICE_XPATH = './/div[@class="classified-price"]/span/text()'

    PRICE_REPLACE_VALUE = 'Цена'

    def parse_listing(self, content: str, url: str) -> List[Flat]:
        root = Selector(content)
        flats_elems = root.xpath(self.FLAT_ITEM_XPATH)

        flats = [self._parse_flat(elem, url) for elem in flats_elems]
        return [item for item in flats if item and item.price <= scrapers_settings.max_flat_price]

    def _parse_flat(self, flat_elem: Selector, url: str) -> Optional[Flat]:
        url = self._parse_url(flat_elem, url=url)
        price = self._parse_price(flat_elem)

        if not price:
            return None

        return Flat(
            url=url,
            price=price
        )

    def parse_next_page_url(self, content: str, url: str) -> Optional[str]:
        root = Selector(content)
        next_page_url_path = root.xpath(self.NEXT_PAGE_URL_XPATH).get()

        if not next_page_url_path:
            return None

        full_next_page_url = urljoin(url, next_page_url_path)
        return full_next_page_url

    @logger.catch
    def _parse_url(self, flat_elem: Selector, url: str) -> str:
        flat_url_path = flat_elem.xpath(self.FLAT_URL_XPATH).get()
        full_url = urljoin(url, flat_url_path)
        return full_url

    @logger.catch
    def _parse_price(self, flat_elem: Selector) -> Optional[int]:
        raw_price = flat_elem.xpath(self.FLAT_PRICE_XPATH).get()
        if not raw_price:
            return None

        price = int(raw_price
                    .replace(self.PRICE_REPLACE_VALUE, '')
                    .replace(' ', '')
                    .strip())
        return price
