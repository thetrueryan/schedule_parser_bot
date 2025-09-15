from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver  # type: ignore[import-untyped]
from fake_useragent import UserAgent

from src.core.settings import settings
from src.handlers.basic_handlers import router as basic_router
from src.handlers.start_handlers import router as start_router
from src.core.middlewares import BotMiddleware


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
    return webdriver.Chrome(options=options)


def setup_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.update.middleware(BotMiddleware())
    dp.include_router(start_router)
    dp.include_router(basic_router)
    return dp


bot = setup_bot()
dp = setup_dispatcher()

driver = setup_driver()
