import pytest

from datetime import datetime

from src.utils.parser_utils import to_day_format_id, get_day_ids


def test_get_day_ids(days_ahead: int = 7):
    days = get_day_ids(days_ahead)
    assert len(days) == days_ahead
    for date in days:
        assert datetime.strptime(date, "%Y%m%d")


def test_day_id(day_number: int = 2):
    day = to_day_format_id(day_number)
    assert day == "20250917"
