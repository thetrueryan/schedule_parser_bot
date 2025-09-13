import asyncio

from src.tasks.parser_tasks import start_parser_loop
from src.core.config import bot, dp, logger


async def main():
    asyncio.create_task(start_parser_loop())
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.info("Program start")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program stop")
