import asyncio

from aiogram import F, Bot, Dispatcher

from app.database.session import Base, engine
from app.bot.handlers.user import handlers as user_handlers
from app.bot.handlers.admin import handlers as admin_handlers
from app.utils import setup_logging

from config import Settings

bot = Bot(token=Settings.token)
dp = Dispatcher()

for _ in user_handlers:
    dp.include_router(_)

for _ in admin_handlers:
    dp.include_router(_)

async def main():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    setup_logging()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())