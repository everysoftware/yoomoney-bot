import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.config import settings
from app.router import router

routers = [router]

bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
dp.include_routers(*routers)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
