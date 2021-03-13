import src.core.logs as logger
from src.bot.bot import BotService

if __name__ == '__main__':
    logger.init_logger()

    bot = BotService()
    bot.get_bot_info()
