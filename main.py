import asyncio

from aiogram import F, Bot, Dispatcher

from app.database.session import Base, engine
from app.bot.handler.start import router as start_router
from app.utils import setup_logging

from config import Settings

bot = Bot(token=Settings.token)
dp = Dispatcher()

dp.include_router(router=start_router)

async def main():
    Base.metadata.create_all(bind=engine)
    setup_logging()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())