from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]

created_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE ('utc', now())"))
]


class Base(DeclarativeBase): ...


class ScheduleOrm(Base):
    __tablename__ = "schedule"

    id: Mapped[intpk]
    day: Mapped[str] = mapped_column(nullable=True)
    hours: Mapped[str] = mapped_column(nullable=True)
    lesson: Mapped[str] = mapped_column(nullable=True)
    teacher: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[created_at]
