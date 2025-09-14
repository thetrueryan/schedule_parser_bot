from datetime import datetime, timedelta, time

from src.models.sqlmodels import ScheduleOrm


def fill_lessons_on_bot_response(response: str, schedule: list[ScheduleOrm]) -> str:
    lesson_number = 0
    for lesson in schedule:
        lesson_number += 1
        response += (
            "<blockquote>"
            f"<b>#{lesson_number}</b>\n"
            f"<b>📚 Предмет:</b> {lesson.subject}\n"
            f"<b>👤 Преподаватель:</b> {lesson.teacher}\n"
            f"<b>🕘 Время:</b> {lesson.time}\n"
            f"<b>🏫 Аудитория:</b> {lesson.room}\n\n"
            "</blockquote>"
        )
    return response


def get_seconds_to_target(hour: int, minutes: int):
    now = datetime.now()
    target_time = time(hour=hour, minute=minutes)

    target_today = datetime.combine(now.date(), target_time)

    if now > target_today:
        target_today += timedelta(days=1)

    delta = target_today - now
    return int(delta.total_seconds())
