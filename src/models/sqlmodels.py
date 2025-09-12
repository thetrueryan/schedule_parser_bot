from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    ...


class ScheduleOrm(Base):
    __tablename__ = "schedule"

    