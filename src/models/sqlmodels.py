from typing import Annotated
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


intpk = Annotated[int, mapped_column(primary_key=True)]

created_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE ('utc', now())"))
]


class Base(DeclarativeBase): ...


class ScheduleOrm(Base):
    __tablename__ = "schedule"

    id: Mapped[intpk]
    date: Mapped[str]
    subject: Mapped[str]
    teacher: Mapped[str]
    time: Mapped[str]
    room: Mapped[str]
    created_at: Mapped[created_at]
