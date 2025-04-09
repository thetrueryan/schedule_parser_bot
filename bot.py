from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram import F
import asyncio
import json
from datetime import timedelta, datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from dotenv import load_dotenv, find_dotenv
#============================================================================

load_dotenv(find_dotenv())

#Инициализация бота
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
GROUP_ID = -1002633208903
#============================================================================



#Команда /START
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    today = datetime.now().date()
    max_date = today + timedelta(weeks=4)
    start_text = (
        '<b>🗓Привет!\n Я бот, который показывает расписание группы БУ-23! \n\n</b>'
        '<blockquote>'
        'Чтобы получить расписание на нужный день, введи:\n'
       ' <code>/расписание ДД.ММ.ГГГГ</code>\n'
       ' Или просто:\n <code>расписание ДД.ММ.ГГГГ</code>\n\n'
        '</blockquote>'
        '<b>Пример: <i>расписание 07.04.2025</i></b>\n\n'
        '<b><u>ВАЖНО‼️\n</u></b>'
        '<blockquote>'
        f'-Введенная дата должна быть не раньше сегодняшнего дня ({today})!\n'
        f'-Введенная дата должна быть до {max_date.strftime('%d.%m.%Y')}!'
        '</blockquote>'
    )
    await message.answer(start_text, parse_mode="HTML")
#============================================================================



#Команда /расписание
@dp.message(Command("расписание"))
@dp.message(F.text.lower().startswith("расписание "))
async def get_schedule(message: types.Message):
    parts = message.text.split()
    
    if len(parts) != 2:
        await message.answer("Введи: расписание ДД.ММ.ГГГГ")
        return
        
    raw_date = parts[1]
    if len(raw_date) != 10:
        await message.answer("Формат даты: ДД.ММ.ГГГГ (например: 05.04.2024)")
        return
    
    try:
        date = raw_date[6:10] + raw_date[3:5] + raw_date[0:2]
        #загрузка файла
        with open("./schedule.json", "r", encoding="utf-8") as f:
            schedule = json.load(f)

        response = f"<b><u>📅 Расписание на {raw_date}:</u></b>\n\n"

        if not schedule[date]:
            response += ("<blockquote><b>#1\n 🤩 ВЫХОДНОЙ </b></blockquote>")
            await message.answer(response, parse_mode="HTML")
            return

        lessons = schedule[date]
        for idx, lesson in enumerate(lessons, start=1):
            if "subject" in lesson:
                response += (
                    "<blockquote>"
                    f"<b>#{idx}</b>\n"
                    f"<b>📚 Предмет:</b> {lesson['subject']}\n"
                    f"<b>👤 Преподаватель:</b> {lesson['teacher']}\n"
                    f"<b>🕘 Время:</b> {lesson['time']}\n"
                    f"<b>🏫 Аудитория:</b> {lesson['room']}\n\n"
                    "</blockquote>"
                )      
        await message.answer(response, parse_mode="HTML")
    except Exception:
        await message.answer("<b>⚠️Ошибка при получении расписания!</b>", parse_mode="HTML")
#============================================================================


#Ежедневная отправка расписания в 10-00 по мск (время можно настроить)
async def send_daily():
    try:
        next_day = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
        date_key = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")

        with open("./schedule.json", "r", encoding="utf-8") as f:
            schedule = json.load(f)

        if date_key not in schedule:
            response = f"📅 Расписание на {next_day}:\n\nРасписание не найдено"
        elif not schedule[date_key]:
            response = f"📅 Расписание на {next_day}:\n <blockquote><b>#1\n 🤩 ВЫХОДНОЙ </b></blockquote>"
        else:
            response = f"<b>📅 Авто-отправка расписания на {next_day}:</b>\n\n"
            for idx, lesson in enumerate(schedule[date_key], start=1):
                response += (
                    "<blockquote>"
                    f"<b>#{idx}</b>\n"
                    f"<b>📚 Предмет:</b> {lesson['subject']}\n"
                    f"<b>👤 Преподаватель:</b> {lesson['teacher']}\n"
                    f"<b>🕘 Время:</b> {lesson['time']}\n"
                    f"<b>🏫 Аудитория:</b> {lesson['room']}\n\n"
                    "</blockquote>"
                )      
        await bot.send_message(
            chat_id=GROUP_ID,
            text=response,
            parse_mode="HTML"
            )
    except Exception as e:
        print(f"ошибка: {e}")
#============================================================================


#Главная функция
async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        send_daily,
        trigger="cron",
        hour=10,
        minute=0,  # Через 1 минуту
        day="*"
    )
    scheduler.start()
    await dp.start_polling(bot)
#============================================================================



if __name__ == "__main__":
    asyncio.run(main())