from datetime import datetime, timedelta


def get_day_ids(days_ahead: int = 14):
    today = datetime.today()
    days = []
    for i in range(days_ahead):
        day = today + timedelta(days=i)
        day_id = day.strftime("%Y%m%d")
        days.append(day_id)
    return days


def get_dates_to_parse(days_ahead: int = 14) -> list:
    today = datetime.today()
    dates = [
        datetime(today + timedelta(days=i)).strftime("%Y%m%d")
        for i in range(days_ahead)
    ]
    return dates
