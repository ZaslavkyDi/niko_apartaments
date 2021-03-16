import asyncio

from src.bot.bot import run_bot
from src.core.logs import init_logger
from src.db.database import init_db


async def run_app() -> None:
    init_logger()
    await init_db()
    await run_bot()


if __name__ == '__main__':
    asyncio.run(run_app())
