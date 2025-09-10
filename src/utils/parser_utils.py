from datetime import datetime, timedelta


def get_dates_to_parse(days_ahead: int = 14) -> list:
    today = datetime.today()
    dates = [
        datetime(today + timedelta(days=i)).strftime("%Y%m%d")
        for i in range(days_ahead)
    ]
    return dates
