import asyncio
from datetime import datetime, timedelta
from aiogram import Bot

from src.core.settings import settings
from src.utils.bot_utils import get_seconds_to_target
from src.utils.sql_utils import get_chats_repo, get_schedule_repo
from src.services.bot_service import BotService
from src.core.logger import logger



async def start_notification_loop(
        bot: Bot,
        notification_hour: int = settings.NOTIFICATION_TIME_HOUR, 
        notification_minutes: int = settings.NOTIFICATION_TIME_MINUTES,
        notificate_cycle_sleep_time: int = 86400,
        ):
    to_start_notification_cycle_time = get_seconds_to_target(
                    hour=notification_hour,
                    minutes=notification_minutes
                )
    logger.info(f"Start waiting {to_start_notification_cycle_time} seconds for notification cycle")
    await asyncio.sleep(to_start_notification_cycle_time)
    while True:
        try:
            logger.info(f"Notification cycle started")
            schedule_repo = await get_schedule_repo()
            chats_repo = await get_chats_repo()
            service = BotService(schedule_repo=schedule_repo, chats_repo=chats_repo)
            notificated_chats = await service.get_chats_by_notification_status(
                status=True
            )
            if not notificated_chats:
                logger.info(f"No chats to send notification. sleep for {notificate_cycle_sleep_time} seconds..")
                await asyncio.sleep(notificate_cycle_sleep_time)
            notificated_date = datetime.today() + timedelta(days=1)
            schedule = await service.get_schedule(notificated_date)
            response = await service.create_schedule_response(
                schedule=schedule, date=notificated_date
            )
            for chat in notificated_chats:
                await bot.send_message(chat_id=chat.chat_id, text=response)
                await asyncio.sleep(1)

            logger.info(f"Notification cycle ended successfully, sleep for {notificate_cycle_sleep_time} seconds..")
            await asyncio.sleep(notificate_cycle_sleep_time)
        except Exception as e:
            logger.error(f"Error in notification cycle: {e}")
            await asyncio.sleep(notificate_cycle_sleep_time)
