from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.services.bot_service import BotService
from src.core.logger import logger

router = Router(name="start_router")


@router.message(Command("start"))
async def start_cmd(message: Message, service: BotService):
    try:
        if message.from_user:
            chat_id = message.from_user.id
            await service.add_new_chat(chat_id)
    except Exception as e:
        logger.error(f"Error in chat with id:{chat_id} while /start command: {e}")

    start_text = await service.get_start_text()
    await message.answer(start_text)
