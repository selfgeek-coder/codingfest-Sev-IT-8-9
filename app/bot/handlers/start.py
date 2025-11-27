from aiogram import Router, F
from aiogram.types import Message

from app.services.user_service import UserService
from app.database.database import get_db

from ..keyboards.main_menu import get_main_keyboard

router = Router()
user_service = UserService()

@router.message(
        F.text == "/start"
        )
async def start(message: Message):
    with get_db() as db:
        user = user_service.create_user(
            db=db,
            chat_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )

    await message.answer(
        f"Привет, {message.from_user.first_name}.\n\nВ этом боте ты можешь заказать *печатную продукцию*",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )