from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.services.user_service import UserService
from app.database.database import get_db
from ...keyboards.user.main_menu import get_main_keyboard

router = Router()
user_service = UserService()

@router.message(Command("start"))
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


@router.callback_query(F.data == "main_menu")
async def start(callback: CallbackQuery):
    with get_db() as db:
        user = user_service.create_user(
            db=db,
            chat_id=callback.from_user.id,
            username=callback.from_user.username,
            first_name=callback.from_user.first_name,
            last_name=callback.from_user.last_name
        )

    await callback.message.edit_text(
        f"Привет, {callback.from_user.first_name}.\n\n"
        f"В этом боте ты можешь заказать *печатную продукцию*",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

    await callback.answer()
