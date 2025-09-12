import asyncio

from src.core.config import logger
from src.services.parser_service import ParserService
from src.utils.parser_utils import get_day_ids
from src.utils.sql_utils import get_schedule_repo


async def start_parser_loop(parser: ParserService, sleep_time: int = 43200):
    while True:

        dates = get_day_ids()
        parser.login()
        schedule = {}
        for date in dates:
            schedule_on_date = parser.parse_day_with_click(date)
            schedule.update(schedule_on_date)
        schedule_list = parser.to_clear_schedule_list(schedule=schedule)
        repo = await get_schedule_repo()
        await parser.update_schedule_in_db(schedule=schedule_list, repo=repo)
        logger.info(f"Schedule parse and add succesfully")

        logger.info(f"parsing cycle completed. sleep on {sleep_time} seconds..")
        await asyncio.sleep(sleep_time)
