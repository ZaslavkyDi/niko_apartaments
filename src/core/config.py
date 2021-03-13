import os

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    bot_api_token: str = str(os.getenv('BOT_API_TOKEN'))


app_settings = AppSettings()
