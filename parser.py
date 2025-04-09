from datetime import datetime, timedelta
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException
import json
from dotenv import load_dotenv, find_dotenv
import os
import tempfile
import shutil
#================================================================
profile_path = tempfile.mkdtemp()

#Ссылки и глобальные переменные:
url = "https://dnevnik.ru/"
day_ids = []
schedule = {}
load_dotenv(find_dotenv())
#================================================================





#Вход в dnevnik.ru:
def dnevnik_login():
    try:
        driver.get(url)
        try:
            driver.find_element(by=By.XPATH, value='//*[@id="anon-buttons"]/div[1]/a').click()
            driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div/div/form/div[2]/div[3]/div[1]/div[1]/label/input').send_keys(os.getenv('LOGIN'))
            driver.find_element(by=By.XPATH, value='//*[@id="password-field"]').send_keys(os.getenv('PASSWD'))
            driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div/div/form/div[2]/div[3]/div[4]/div[1]/input').click()
            driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[2]/ul/li[2]/ul/li[4]/a').click()  
        except Exception as e:
            print(f"Ошибка, элемент не найден или отсутствует: {e}")
        time.sleep(2)
    except Exception as e:
        print(f"Ошибка загрузки страницы: {e}")    
#================================================================


#Формируем список с актуальными датами
def get_day_ids(days_ahead=28):
    today = datetime.today()
    for i in range(days_ahead):
        day = today + timedelta(days=i)
        day_id = day.strftime("%Y%m%d")  
        day_ids.append(day_id)
    return day_ids
#================================================================


#Парсим рассписание на день, и если такого дня нет, переключаем на следующую неделю
def parse_day_with_click(day_id):
    found = False
    attempts = 0
    while not found and attempts < 3:  
        try:
            for i in range(1, 6):
                para_element = driver.find_element(by=By.XPATH, value=f'//*[@id="d{day_id}_{i}"]')
                para = para_element.text.strip()
                if para:
                    schedule[day_id].append(para)
            found = True  
        except NoSuchElementException:
            print(f"День {day_id} не найден на текущей неделе, переключаю...")
            try:
                driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul[1]/li[2]/a').click()
                time.sleep(2)  
                attempts += 1
            except Exception as e:
                print(f"Ошибка при переключении недели: {e}")
                break
#================================================================


#Формируем итоговый словарь для записи:
def schedule_save():
    cleaned_schedule = {}
    SUBJECT_REPLACEMENTS = {
        "МДК 01.01 Пр...": "МДК 01.01 Практические занятия",
        "МДК 01.01 1С...": "МДК 01.01 1С",
        "МДК 04.02 ос...": "МДК 04.02 Статистика",
        "Налоги и нал...": "Налоги и налогообложение",
        "Экономика ор...": "Экономика организации",
        "МДК 05.01 Ве...": "МДК 05.01 Касса"
    }
    for date, lessons in schedule.items():
        cleaned_lessons = []
        for lesson in lessons:
            parts = [part.strip() for part in lesson.split('\n')]
            if len(parts) == 4:
                cleaned_lessons.append({
                    "subject": parts[0],
                    "teacher": parts[1],
                    "time": parts[2],
                    "room": parts[3]
                }) 
            elif len(parts) == 8:
                cleaned_lessons.append({
                    "subject": parts[4],
                    "teacher": parts[1]+ ", " + parts[5],
                    "time": parts[2],
                    "room": parts[3] + ", " + parts[-1] 
                })       
            else:
                cleaned_lessons.append({"raw": lesson})
        
            for lesson in cleaned_lessons:
                if "subject" in lesson:
                    original = lesson["subject"]
                    lesson["subject"] = SUBJECT_REPLACEMENTS.get(original, original)
    
        cleaned_schedule[date] = cleaned_lessons
    with open("./schedule.json", "w", encoding='utf-8') as f:
        json.dump(cleaned_schedule, f, ensure_ascii=False, indent=4)
    print("Расписание сохранено в словарь.")
#================================================================


#Главная функция
def main():
    global driver, schedule
    # Инициализация драйвера при каждом запуске
    options = Options()
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    day_ids = get_day_ids()
    schedule = {day_id: [] for day_id in day_ids}  
    dnevnik_login()

    for day_id in day_ids:
        parse_day_with_click(day_id)
    schedule_save()
#================================================================    


if __name__ == "__main__":
    try:
        main()
        print(f"Скрипт начался: {datetime.now()}")
    except Exception as e:
        print(f"[Ошибка во время работы скрипта]: {e}")
    finally:
        if driver:
            driver.quit()
            shutil.rmtree(profile_path, ignore_errors=True)



