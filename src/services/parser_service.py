import time
from datetime import datetime
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from src.repository.schedule_repository import ScheduleRepository
from src.core.config import driver, logger
from src.core.settings import settings


class ParserService:
    def __init__(self, driver: webdriver.Chrome = driver):
        self.driver = driver

    def login(self) -> None:
        try:
            self.driver.get(settings.DNEVNIK_URL)
            self.driver.find_element(
                by=By.XPATH, value='//*[@id="anon-buttons"]/div[1]/a'
            ).click()
            self.driver.find_element(
                by=By.XPATH,
                value="/html/body/div/div/div/div/div/form/div[2]/div[3]/div[1]/div[1]/label/input",
            ).send_keys(settings.DNEVNIK_LOGIN)
            self.driver.find_element(
                by=By.XPATH, value='//*[@id="password-field"]'
            ).send_keys(settings.DNEVNIK_PASS)
            self.driver.find_element(
                by=By.XPATH,
                value="/html/body/div/div/div/div/div/form/div[2]/div[3]/div[4]/div[1]/input",
            ).click()
            self.driver.find_element(
                by=By.XPATH, value="/html/body/div[2]/div/div[2]/ul/li[2]/ul/li[4]/a"
            ).click()
            logger.info("login complete succesfuly")
            time.sleep(2)
        except NoSuchElementException as e:
            logger.error(f"Cant find element while login: {e}")
            raise NoSuchElementException
        except Exception as e:
            logger.error(f"Error while login: {e}")
            raise

    def parse_day_with_click(
        self,
        date: datetime,
        max_att: int = 3,
        max_lessons: int = 6,
        schedule_on_this_date: dict = {},
    ):
        attempts = 0
        while attempts < max_att:
            try:
                for i in range(1, max_lessons):
                    para_element = self.driver.find_element(
                        by=By.XPATH, value=f'//*[@id="d{date}_{i}"]'
                    )
                    para = para_element.text.strip()
                    if para:
                        if date not in schedule_on_this_date:
                            schedule_on_this_date.update({date: []})
                        else:
                            schedule_on_this_date[date].append(para)
                return schedule_on_this_date
            except NoSuchElementException:
                logger.warning(f"day {date} not found, trying search on next week..")
                try:
                    self.driver.find_element(
                        by=By.XPATH, value='//*[@id="content"]/div[3]/ul[1]/li[2]/a'
                    ).click()
                    time.sleep(2)
                    attempts += 1
                except Exception as e:
                    logger.error(f"Error while switching week: {e}")
                    break

    def to_clear_schedule_list(self, schedule: dict) -> list:
        clear_schedule = []
        for date, lessons in schedule.items():
            for lesson in lessons:
                parts = [part.strip() for part in lesson.split("\n")]
                if len(parts) == 4:
                    clear_schedule.append(
                        {
                            "date": date,
                            "subject": parts[0],
                            "teacher": parts[1],
                            "time": parts[2],
                            "room": parts[3],
                        }
                    )
                elif len(parts) == 8:
                    clear_schedule.append(
                        {
                            "date": date,
                            "subject": parts[4],
                            "teacher": parts[1] + ", " + parts[5],
                            "time": parts[2],
                            "room": parts[3] + ", " + parts[-1],
                        }
                    )
                else:
                    continue
        return clear_schedule

    async def update_schedule_in_db(
        self, schedule: list[dict], repo: ScheduleRepository
    ) -> None:
        status = await repo.add_schedule(schedule)
        if not status:
            logger.warning(f"schedule dont added in db: {schedule}")
        return None
