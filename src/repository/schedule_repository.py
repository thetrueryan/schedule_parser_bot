from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete

from src.models.sqlmodels import ScheduleOrm
from src.core.logger import logger


class ScheduleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_schedule(self, schedule: list[dict]) -> bool:
        try:
            unique_dates = {item["date"] for item in schedule}
            for date in unique_dates:
                delete_stmt = delete(ScheduleOrm).where(ScheduleOrm.date == date)
                await self.session.execute(delete_stmt)

            stmt = insert(ScheduleOrm)
            await self.session.execute(stmt, schedule)
            await self.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error while add schedule in db: {e}")
            await self.session.rollback()
            return False

    async def get_schedule_by_date(self, date: str):
        stmt = select(ScheduleOrm).where(ScheduleOrm.date == date)
        result = await self.session.execute(stmt)
        return result.scalars().all()
