import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from fake_useragent import UserAgent

from src.core.settings import settings

BASE_PATH = Path(__file__).resolve().parent.parent.parent

logger_path = BASE_PATH / "logs" / "app_logs.log"
logger_path.parent.mkdir(parents=True, exist_ok=True)


def setup_logger(lvl: int = logging.INFO) -> Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(level=lvl)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )

    file_handler = RotatingFileHandler(
        logger_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def setup_bot() -> Bot:
    if settings.BOT_TOKEN:
        return Bot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
    else:
        raise ValueError("Bot token is None!")


def setup_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        options=options,
    )


logger = setup_logger()

bot = setup_bot()
dp = Dispatcher()

driver = setup_driver()
