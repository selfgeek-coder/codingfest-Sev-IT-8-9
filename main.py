import asyncio

from aiogram import F, Bot, Dispatcher

from app.database.session import Base, engine
from app.bot.handlers.start import router as start_router
from app.bot.handlers.order import router as order_router
from app.utils import setup_logging

from config import Settings

bot = Bot(token=Settings.token)
dp = Dispatcher()

dp.include_router(router=start_router)
dp.include_router(router=order_router)

async def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    setup_logging()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())