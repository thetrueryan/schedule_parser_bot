from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram import F
import asyncio
import json
from datetime import timedelta, datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import os
from dotenv import load_dotenv, find_dotenv
from parser import run_parser
#============================================================================


#Инициализация бота
load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
GROUPS_FILE = "./groups.json"
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
        with open(GROUPS_FILE, "r", encoding="utf-8") as f:
            groups = json.load(f)


        if date_key not in schedule:
            response = f"📅 Расписание на {next_day}:\n\nРасписание не найдено"
        elif not schedule[date_key]:
            response = f"📅 Расписание на {next_day}:\n <blockquote><b>#1\n 🤩 ВЫХОДНОЙ </b></blockquote>"
        else:
            response = f"<b><u>📅 Авто-отправка расписания на {next_day}:</u></b>\n\n"
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
        for group_id in groups:
            try:
                await bot.send_message(
                    chat_id=group_id,
                    text=response,
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Ошибка при отправке в {group_id}: {e}")
    except Exception as e:
        print(f"ошибка: {e}")
#============================================================================


#Функция загрузки/добавления чатов для рассылки
def save_id(chat_id: int):
    try:
        with open(GROUPS_FILE, "r", encoding="utf-8") as f:
            groups = json.load(f)
    except:
        groups = []
    
    if chat_id not in groups:
        groups.append(chat_id)
        with open(GROUPS_FILE, "w", encoding="utf-8") as f:
            json.dump(groups, f, indent=2)
        return True
    return False
#============================================================================


#Комманда добавления чата в файл для рассылки
@dp.message(Command("добавить"))
@dp.message(F.text.lower().startswith("добавить "))
async def add_chat_id(message: types.Message):
    if save_id(message.chat.id):
        await message.reply("✅Чат успешно добавлен в рассылки!")
    else:
        await message.reply("ℹ️ Группа уже есть в списке!")
#============================================================================


#Главная функция
async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
   # Задания на регулярный парсинг (00:00, 06:00, 12:00, 18:00, 00:00)
    scheduler.add_job(run_parser, CronTrigger(hour='0,6,12,18', minute=0))

    # Парсинг перед автоотправкой в 10:00
    scheduler.add_job(run_parser, CronTrigger(hour=9, minute=55))

    # Отправка расписания в 10:00
    scheduler.add_job(send_daily, CronTrigger(hour=10, minute=0))
    scheduler.start()
    await dp.start_polling(bot)
#============================================================================


if __name__ == "__main__":
    asyncio.run(main())