from datetime import datetime, timedelta

from src.core.settings import settings


def to_day_format_id(day_number: int) -> str:
    day = datetime.today() + timedelta(days=day_number)
    return day.strftime("%Y%m%d")


def get_day_ids(days_ahead: int = settings.WEEKS_TOTAL * 7):
    if days_ahead < 7:
        raise ValueError("WEEKS_TOTAL cant be less than 1")
    days = [to_day_format_id(day_number) for day_number in range(days_ahead)]
    return days
