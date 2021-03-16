import asyncio

from tortoise import Tortoise, run_async

from src.core.config import app_settings


async def init_db() -> None:
    await Tortoise.init(
        db_url=app_settings.db_url,
        modules={'models': ['src.db.models']}
    )
    await Tortoise.generate_schemas()

