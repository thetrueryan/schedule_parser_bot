from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src.services.bot_service import BotService
from src.core.exc import DateValidateException
from src.core.logger import logger
from src.core.settings import settings

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
        await message.answer("⚠️Ошибка при получении расписания!")


@router.message(Command("добавить"))
async def add_chat_id(message: Message, service: BotService):
    try:
        if message.from_user:
            chat_id = message.from_user.id
            status = await service.set_notification_status_in_chat(
                chat_id=chat_id, status=True
            )
            if not status:
                raise
            await message.answer(
                f"✅Чат успешно добавлен в ежедневную рассылку в {settings.NOTIFICATION_TIME_HOUR}:{settings.NOTIFICATION_TIME_MINUTES}!"
            )
            logger.info(
                f"Chat with id: {chat_id} subscribe to notifications successfully"
            )
    except Exception as e:
        logger.error(f"Error while add chat: {chat_id} to notification system: {e}")
        await message.answer("⚠️Ошибка при добавлении чата в ежедневную рассылку!")


@router.message(Command("удалить"))
async def remove_chat_id(message: Message, service: BotService):
    try:
        if message.from_user:
            chat_id = message.from_user.id
            status = await service.set_notification_status_in_chat(
                chat_id=chat_id, status=False
            )
            if not status:
                raise
            await message.answer(
                f"✅Чат успешно удален из ежедневной рассылки в {settings.NOTIFICATION_TIME_HOUR}:{settings.NOTIFICATION_TIME_MINUTES}!"
            )
            logger.info(
                f"Chat with id: {chat_id} subscribe to notifications successfully"
            )
    except Exception as e:
        logger.error(f"Error while add chat: {chat_id} to notification system: {e}")
        await message.answer("⚠️Ошибка при удалении чата из ежедневной рассылки!")
