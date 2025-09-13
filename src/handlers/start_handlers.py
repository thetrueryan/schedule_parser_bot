from datetime import datetime, timedelta

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from src.core.settings import settings

router = Router(name="start_router")


@router.message(Command("start"))
async def start_cmd(message: Message):
    today = datetime.now().date()
    max_date = today + timedelta(weeks=settings.WEEKS_TOTAL)
    start_text = (
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
    await message.answer(start_text)
