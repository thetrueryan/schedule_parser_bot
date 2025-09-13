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
