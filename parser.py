from datetime import datetime, timedelta
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException
import json
from dotenv import load_dotenv, find_dotenv
import os

# ================================================================


# Ссылки и глобальные переменные:
url = "https://dnevnik.ru/"
day_ids = []
schedule = {}
load_dotenv(find_dotenv())
# ================================================================


# Формируем driver и options
options = Options()
options.add_argument(f"user-agent={UserAgent().random}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(
    options=options,
)
# ================================================================


# Вход в dnevnik.ru:
def login():
    try:
        driver.get(url)
        try:
            driver.find_element(
                by=By.XPATH, value='//*[@id="anon-buttons"]/div[1]/a'
            ).click()
            driver.find_element(
                by=By.XPATH,
                value="/html/body/div/div/div/div/div/form/div[2]/div[3]/div[1]/div[1]/label/input",
            ).send_keys(os.getenv("LOGIN"))
            driver.find_element(
                by=By.XPATH, value='//*[@id="password-field"]'
            ).send_keys(os.getenv("PASSWD"))
            driver.find_element(
                by=By.XPATH,
                value="/html/body/div/div/div/div/div/form/div[2]/div[3]/div[4]/div[1]/input",
            ).click()
            driver.find_element(
                by=By.XPATH, value="/html/body/div[2]/div/div[2]/ul/li[2]/ul/li[4]/a"
            ).click()
        except Exception as e:
            print(f"Ошибка, элемент не найден или отсутствует: {e}")
        time.sleep(2)
    except Exception as e:
        print(f"Ошибка загрузки страницы: {e}")


# ================================================================


# Формируем список с актуальными датами
def get_day_ids(days_ahead=28):
    today = datetime.today()
    for i in range(days_ahead):
        day = today + timedelta(days=i)
        day_id = day.strftime("%Y%m%d")
        day_ids.append(day_id)
    return day_ids


# ================================================================


# Парсим рассписание на день, и если такого дня нет, переключаем на следующую неделю
def parse_day_with_click(day_id):
    found = False
    attempts = 0
    while not found and attempts < 3:
        try:
            for i in range(1, 6):
                para_element = driver.find_element(
                    by=By.XPATH, value=f'//*[@id="d{day_id}_{i}"]'
                )
                para = para_element.text.strip()
                if para:
                    schedule[day_id].append(para)
            found = True
        except NoSuchElementException:
            print(f"День {day_id} не найден на текущей неделе, переключаю...")
            try:
                driver.find_element(
                    by=By.XPATH, value='//*[@id="content"]/div[3]/ul[1]/li[2]/a'
                ).click()
                time.sleep(2)
                attempts += 1
            except Exception as e:
                print(f"Ошибка при переключении недели: {e}")
                break


# ================================================================


# Формируем итоговый словарь для записи:
def schedule_save():
    cleaned_schedule = {}
    for date, lessons in schedule.items():
        cleaned_lessons = []
        for lesson in lessons:
            parts = [part.strip() for part in lesson.split("\n")]
            if len(parts) == 4:
                cleaned_lessons.append(
                    {
                        "subject": parts[0],
                        "teacher": parts[1],
                        "time": parts[2],
                        "room": parts[3],
                    }
                )
            elif len(parts) == 8:
                cleaned_lessons.append(
                    {
                        "subject": parts[4],
                        "teacher": parts[1] + ", " + parts[5],
                        "time": parts[2],
                        "room": parts[3] + ", " + parts[-1],
                    }
                )
            else:
                cleaned_lessons.append({"raw": lesson})

        cleaned_schedule[date] = cleaned_lessons
    with open("./schedule.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_schedule, f, ensure_ascii=False, indent=4)
    print("Расписание сохранено в словарь.")


# ================================================================


# Главная функция
def run_parser():
    global driver, schedule
    try:
        day_ids = get_day_ids()
        schedule = {day_id: [] for day_id in day_ids}
        login()
        for day_id in day_ids:
            parse_day_with_click(day_id)
        schedule_save()

    except Exception as e:
        print(f"[Ошибка во время работы скрипта]: {e}")
    finally:
        if driver:
            driver.quit()


# ================================================================
run_parser()