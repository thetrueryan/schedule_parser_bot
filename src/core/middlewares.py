from aiogram import BaseMiddleware

from src.services.bot_service import BotService
from src.repository.schedule_repository import ScheduleRepository
from src.utils.sql_utils import get_schedule_repo, get_chats_repo


class BotMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if not hasattr(self, "schedule_repo"):
            self.schedule_repo = await get_schedule_repo()

        if not hasattr(self, "chats_repo"):
            self.chats_repo = await get_chats_repo()

        if not hasattr(self, "service"):
            self.service = BotService(self.schedule_repo, self.chats_repo)

        data["service"] = self.service

        return await handler(event, data)
