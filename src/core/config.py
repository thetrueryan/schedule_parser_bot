from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

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


def setup_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.update.middleware(BotMiddleware())
    dp.include_router(start_router)
    dp.include_router(basic_router)
    return dp


bot = setup_bot()
dp = setup_dispatcher()
