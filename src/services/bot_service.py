from datetime import datetime

from src.repository.schedule_repository import ScheduleRepository
from src.core.exc import DateValidateException
from src.utils.bot_utils import fill_lessons_on_bot_response
from src.core.config import logger


class BotService:
    def __init__(self, repo: ScheduleRepository):
        self.repo = repo

    async def get_date_from_message(self, message: str) -> str:
        parts = message.text.split()
        if len(parts) != 2:
            raise DateValidateException

        date = parts[1]
        if len(date) != 10:
            raise DateValidateException

        return date

    async def get_schedule(self, date: str) -> list | None:
        format_date = date[6:10] + date[3:5] + date[0:2]
        schedule = await self.repo.get_schedule_by_date(format_date)
        return schedule

    async def create_schedule_response(self, schedule: list, date: str):
        response = f"<b><u>📅 Расписание на {date}:</u></b>\n\n"

        if not schedule:
            response += "<blockquote><b>#1\n 🤩 ВЫХОДНОЙ </b></blockquote>"
            return response
        response = fill_lessons_on_bot_response(response=response, schedule=schedule)
        return response
