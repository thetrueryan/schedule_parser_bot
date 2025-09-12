from src.core.session import async_session_factory
from src.repository.schedule_repository import ScheduleRepository


async def get_session():
    async with async_session_factory() as session:
        yield session


async def get_schedule_repo() -> ScheduleRepository:
    session = await get_session()
    return ScheduleRepository(session=session)
