import os

import dotenv
from pydantic import BaseSettings

env_file_path = dotenv.find_dotenv()
dotenv.load_dotenv(env_file_path)


class AppSettings(BaseSettings):
    debug: bool = os.getenv('DEBUG', False)
    bot_api_token: str = os.getenv('BOT_API_TOKEN')
    bot_channel_id: str = os.getenv('BOT_CHANNEL_ID')
    db_url: str = os.getenv('DB_URL')


app_settings = AppSettings()
