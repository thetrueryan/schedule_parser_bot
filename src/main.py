import asyncio

from src.tasks.parser_tasks import start_parser_loop
from src.tasks.bot_tasks import start_notification_loop
from src.core.config import bot, dp
from src.core.logger import logger


async def main():
    polling_task = asyncio.create_task(dp.start_polling(bot))
    await asyncio.sleep(2)

    asyncio.create_task(start_parser_loop())
    asyncio.create_task(start_notification_loop(bot))

    await polling_task


if __name__ == "__main__":
    try:
        logger.info("Program start")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program stop")
