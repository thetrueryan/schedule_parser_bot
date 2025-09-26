from datetime import datetime, timedelta

from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver  # type: ignore[import-untyped]
from fake_useragent import UserAgent

from src.core.settings import settings
from src.services.parser_service import ParserService
from src.utils.sql_utils import get_schedule_repo


def to_day_format_id(day_number: int) -> str:
    day = datetime.today() + timedelta(days=day_number)
    return day.strftime("%Y%m%d")


def get_day_ids(days_ahead: int = settings.WEEKS_TOTAL * 7):
    if days_ahead < 7:
        raise ValueError("WEEKS_TOTAL cant be less than 1")
    days = [to_day_format_id(day_number) for day_number in range(days_ahead)]
    return days


def get_webdriver() -> webdriver.Chrome:
    options = Options()
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


async def get_parser_service() -> ParserService:
    repo = await get_schedule_repo()
    driver = get_webdriver()
    return ParserService(repo=repo, driver=driver)
