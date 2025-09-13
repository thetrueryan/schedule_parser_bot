from aiogram import BaseMiddleware

from src.services.bot_service import BotService
from src.repository.schedule_repository import ScheduleRepository


class BotMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if not hasattr(self, "repo"):
            self.repo = await ScheduleRepository.create()
            self.service = BotService(self.repo)

        data["service"] = self.service
        data["repository"] = self.repo

        return await handler(event, data)
