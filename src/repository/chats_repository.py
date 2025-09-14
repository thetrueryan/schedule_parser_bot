from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update
from sqlalchemy.exc import IntegrityError

from src.models.sqlmodels import ChatsOrm
from src.core.logger import logger


class ChatsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_chat(self, chat_id: int) -> bool:
        try:
            stmt = insert(ChatsOrm).values(chat_id=chat_id)
            await self.session.execute(stmt)
            await self.session.commit()
            return True
        except IntegrityError:
            return False

    async def update_notification_status(self, chat_id: int, status: bool) -> bool:
        try:
            stmt = (update(ChatsOrm).where(ChatsOrm.chat_id == chat_id)).values(
                notification_status=status
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error while update chat notification status: {e}")
            return False
