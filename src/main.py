from src.scripts.parser_scripts import start_parser_loop
from src.services.parser_service import ParserService
from src.core.config import bot, dp


async def main():
    parser = ParserService()
    await start_parser_loop(parser)
    await dp.start_polling(bot)
