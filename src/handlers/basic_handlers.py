from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src.services.bot_service import BotService
from src.core.exc import DateValidateException
from src.core.logger import logger

router = Router(name="base_router")


@router.message(Command("расписание"))
@router.message(F.text.lower().startswith("расписание "))
async def get_schedule(message: Message, service: BotService):
    try:
        date = await service.get_date_from_message(message)
        schedule = await service.get_schedule(date)
        response = await service.create_schedule_response(schedule=schedule, date=date)
        await message.answer(response)
    except DateValidateException:
        await message.answer(
            "Введите дату в формате: ДД.ММ.ГГГГ (например: 05.04.2025)"
        )
    except Exception as e:
        logger.error(f"Error while user get schedule: {e}")
        await message.answer("<b>⚠️Ошибка при получении расписания!</b>")
