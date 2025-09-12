from sqlalchemy.ext.asyncio import AsyncSession

class ScheduleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session