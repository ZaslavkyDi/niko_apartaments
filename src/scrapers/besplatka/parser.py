from typing import List, Optional, Dict
from urllib.parse import urljoin

from loguru import logger
from parsel import Selector

from src.db.models import Flat


class BesplatkaParse:
    NEXT_PAGE_XPATH = '//li[@class="next"]/a/@href'
    FLAT_ITEM_XPATH = '//div[@class="group-title is_not_shop"][last()]/following-sibling::div[@class="messages-list"]/div'
    FLAT_URL_XPATH = './*/a/@href'
    FLAT_PRICE_XPATH = './/p[@class="m-price"]/span/text()'

    def parse_listing(self, content: str, url: str) -> List[Flat]:
        root = Selector(content)
        flats_elems = root.xpath(self.FLAT_ITEM_XPATH)

        flats = [self._parse_flat_elem(elem, url) for elem in flats_elems]
        return [item for item in flats if item]

    @logger.catch
    def parse_next_page_url(self, content: str, url=None) -> Optional[str]:
        root = Selector(content)
        next_page_url_path = root.xpath(self.NEXT_PAGE_XPATH).get()

        return urljoin(url, next_page_url_path) if next_page_url_path else None

    @logger.catch
    def _parse_flat_elem(self, flat_elem: Selector, url: str) -> Optional[Flat]:
        url = self._parse_url(flat_elem, url=url)
        price = self._parse_price(flat_elem)

        if price:
            return Flat(
                url=url,
                price=price
            )

    @logger.catch
    def _parse_url(self, flat_elem: Selector, url: str) -> str:
        url_path = flat_elem.xpath(self.FLAT_URL_XPATH).get()
        return urljoin(url, url_path)

    @logger.catch
    def _parse_price(self, flat_elem: Selector) -> Optional[int]:
        raw_price = flat_elem.xpath(self.FLAT_PRICE_XPATH).get()

        if not raw_price:
            return None

        clean_price = raw_price.replace(' ', '').strip()
        return int(clean_price)
