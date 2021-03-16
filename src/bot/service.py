from typing import List

from src.db.models import Flat


class FlatBotService:
    _BOT_MESSAGE_TEMPLATE = '''
    {source_url}
    {price}
    '''

    @staticmethod
    async def get_fresh_flats() -> List[Flat]:
        fresh_flats = await Flat.filter(is_published=False)
        return fresh_flats

    @staticmethod
    async def mark_flat_as_processed(flat: Flat) -> Flat:
        flat.is_published = True  # type: ignore
        await flat.save()
        return flat

    def generate_bot_message(self, flat: Flat) -> str:
        return self._BOT_MESSAGE_TEMPLATE.format(
            source_url=flat.url,
            price=flat.price
        )
