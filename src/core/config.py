import os

import dotenv
from pydantic import BaseSettings

env_file_path = dotenv.find_dotenv()
dotenv.load_dotenv(env_file_path)


class AppSettings(BaseSettings):
    bot_api_token: str = os.getenv('BOT_API_TOKEN')


app_settings = AppSettings()
