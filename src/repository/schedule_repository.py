from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from src.models.sqlmodels import ScheduleOrm
from src.core.config import logger


class ScheduleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_schedule(self, schedule: list[dict]) -> bool:
        try:
            stmt = insert(ScheduleOrm)
            await self.session.execute(stmt, schedule)
            await self.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error while add schedule in db: {e}")
            return False
