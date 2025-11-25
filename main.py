import asyncio

from aiogram import F, Bot, Dispatcher

from app.database.session import Base, engine
from app.bot.handler.start import router as start_router

from config import Settings

bot = Bot(token=Settings.token)
dp = Dispatcher()

dp.include_router(router=start_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    asyncio.run(main())