from abc import ABC, abstractmethod
from typing import List

from src.db.models import Flat


class BaseParse(ABC):

    @abstractmethod
    def parse_listing(self, content: str, url: str = None) -> List[Flat]:
        pass

    @abstractmethod
    def parse_next_page_url(self, content: str, url = None) -> str:
        pass