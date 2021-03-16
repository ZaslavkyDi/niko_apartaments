from asyncio import sleep

from aiogram import Bot, Dispatcher
from loguru import logger

from src.bot.service import FlatBotService
from src.core.config import bot_settings

app_bot = Bot(token=bot_settings.bot_api_token)
bot_dispatcher = Dispatcher(bot=app_bot)
bot_service = FlatBotService()


async def __publish_data_if_exist() -> None:
    flats = await bot_service.get_fresh_flats()
    for flat in flats:
        message = bot_service.generate_bot_message(flat)
        await app_bot.send_message(
            chat_id=bot_settings.bot_channel_id,
            text=message
        )
        await bot_service.mark_flat_as_processed(flat)


async def run_bot() -> None:
    logger.info('Run bot!')
    while True:
        logger.info('Check updates')
        await __publish_data_if_exist()
        await sleep(10)
