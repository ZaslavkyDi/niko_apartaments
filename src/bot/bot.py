import telegram
from telegram import User

from ..core.config import app_settings


class BotService:

    def __init__(self):
        self._bot = telegram.Bot(token=app_settings.bot_api_token)

    def get_bot_info(self) -> User:
        return self._bot.get_me()
