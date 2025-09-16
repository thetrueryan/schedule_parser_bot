from datetime import datetime, timedelta
from typing import Optional
from aiogram.types import Message

from src.repository.schedule_repository import ScheduleRepository
from src.repository.chats_repository import ChatsRepository
from src.models.sqlmodels import ChatsOrm
from src.core.exc import DateValidateException
from src.utils.bot_utils import fill_lessons_on_bot_response
from src.core.settings import settings


class BotService:
    def __init__(self, schedule_repo: ScheduleRepository, chats_repo: ChatsRepository):
        self.schedule_repo = schedule_repo
        self.chats_repo = chats_repo

    async def get_date_from_message(self, message: Message) -> datetime:
        if not message.text:
            raise DateValidateException

        parts = message.text.split()
        if len(parts) != 2:
            raise DateValidateException

        date = parts[1]
        try:
            return datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            raise DateValidateException

    async def get_schedule(self, date: datetime) -> list:
        try:
            format_date = date.strftime("%Y%m%d")
            schedule = await self.schedule_repo.get_schedule_by_date(format_date)
            return schedule
        except Exception:
            raise

    async def create_schedule_response(self, schedule: list, date: datetime):
        response = f"<b><u>📅 Расписание на {date.strftime("%d.%m.%Y")}:</u></b>\n\n"

        if not schedule:
            response += "<blockquote><b>#1\n 🤩 ВЫХОДНОЙ </b></blockquote>"
            return response
        response = fill_lessons_on_bot_response(response=response, schedule=schedule)
        return response

    async def add_new_chat(self, chat_id: int) -> bool:
        status = await self.chats_repo.add_chat(chat_id)
        return status

    async def get_start_text(self) -> str:
        today = datetime.now().date()
        max_date = today + timedelta(weeks=settings.WEEKS_TOTAL)
        return (
            f"<b>🗓Привет!\n Я бот, который показывает расписание {settings.GROUP_NAME} \n\n</b>"
            "<blockquote>"
            "Чтобы получить расписание на нужный день, введи:\n"
            " <code>/расписание ДД.ММ.ГГГГ</code>\n"
            " Или просто:\n <code>расписание ДД.ММ.ГГГГ</code>\n\n"
            "</blockquote>"
            "<b>Пример: <i>расписание 07.04.2025</i></b>\n\n"
            "<b><u>ВАЖНО‼️\n</u></b>"
            "<blockquote>"
            f"-Введенная дата должна быть не раньше сегодняшнего дня ({today})!\n"
            f"-Введенная дата должна быть до {max_date.strftime('%d.%m.%Y')}!"
            "</blockquote>"
        )

    async def set_notification_status_in_chat(self, chat_id: int, status: bool = True):
        status = await self.chats_repo.update_notification_status(
            chat_id=chat_id, status=status
        )
        return status

    async def get_chats_by_notification_status(
        self, status: bool = True
    ) -> list[ChatsOrm]:
        chat_list = await self.chats_repo.get_chats_by_status(status=status)
        return chat_list

    async def get_help_text(self) -> str:
        today = datetime.now().date()
        max_date = today + timedelta(weeks=settings.WEEKS_TOTAL)
        return (
            "<b>🎓 Помощь по командам бота</b>\n\n"
            "<u>📅 Получение расписания:</u>\n"
            "<code>расписание 15.09.2025</code> - на конкретную дату\n"
            "<code>/расписание 15.09.2025</code> - аналогично\n\n"
            f"-Введенная дата должна быть не раньше сегодняшнего дня ({today})!\n"
            f"-Введенная дата должна быть до {max_date.strftime('%d.%m.%Y')}!"
            "<u>🔔 Управление уведомлениями:</u>\n"
            "<code>/добавить</code> - ✅ Подписаться на рассылку\n"
            "<code>/удалить</code> - ❌ Отписаться от рассылки\n\n"
            "<u>ℹ️ Служебные команды:</u>\n"
            "<code>/start</code> - Перезапустить бота\n"
            "<code>/help</code> - Это сообщение\n\n"
            "<u>⏰ Время рассылки:</u>\n"
            f"Ежедневно в <b>{settings.NOTIFICATION_TIME_HOUR}:{settings.NOTIFICATION_TIME_MINUTES} по МСК</b> вы получаете расписание на следующий учебный день\n\n"
            "<u>📝 Формат даты:</u>\n"
            "Всегда используйте: <code>ДД.ММ.ГГГГ</code> (например: 15.09.2025)"
        )
