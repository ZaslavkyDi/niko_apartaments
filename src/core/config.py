import os

import dotenv
from pydantic import BaseSettings

env_file_path = dotenv.find_dotenv()
dotenv.load_dotenv(env_file_path)


class AppSettings(BaseSettings):
    debug: bool = os.getenv('DEBUG', False)
    db_url: str = os.getenv('DB_URL')
    request_time_out_seconds: int = os.getenv('REQUEST_TIMEOUT_SECONDS', 30)


class BotSettings(AppSettings):
    bot_api_token: str = os.getenv('BOT_API_TOKEN')
    bot_channel_id: str = os.getenv('BOT_CHANNEL_ID')


class ScrapersSettings(AppSettings):
    max_flat_price: int = os.getenv('MAX_FLAT_PRICE')
    scraper_sleep_seconds: int = os.getenv('SCRAPER_SLEEP_SECONDS')
    besplatka_listing_url: str = os.getenv('BESPLATKA_LISTING_URL')
    domria_listing_url: str = os.getenv('DOMRIA_LISTING_URL')
    rieltor_listing_url: str = os.getenv('RIELTOR_LISTING_URL')


app_settings = AppSettings()
bot_settings = BotSettings()
scrapers_settings = ScrapersSettings()
