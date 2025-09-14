from src.core.session import async_session_factory
from src.repository.schedule_repository import ScheduleRepository
from src.repository.chats_repository import ChatsRepository


async def get_session():
    async with async_session_factory() as session:
        yield session


async def get_schedule_repo() -> ScheduleRepository:
    async with async_session_factory() as session:
        return ScheduleRepository(session=session)


async def get_chats_repo() -> ChatsRepository:
    async with async_session_factory() as session:
        return ChatsRepository(session=session)
