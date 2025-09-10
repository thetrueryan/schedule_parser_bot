import asyncio

from services.parser_service import ParserService
from utils.parser_utils import get_dates_to_parse

async def start_parser_loop(parser: ParserService):
    while True:
        dates = get_dates_to_parse()
        parser.login()
        schedule = {}
        for date in dates:
            schedule_on_date = parser.parse_day_with_click(date)
            schedule.update(schedule_on_date)