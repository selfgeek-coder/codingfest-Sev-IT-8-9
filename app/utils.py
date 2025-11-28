import logging

import os
import re
import secrets 
import string

from aiogram import F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from config import Settings

def setup_logging():
    """
    конфигурирует логирование
    формат:
    [INFO] 2025-11-27 20:35:23,143 aiogram.dispatcher: Start polling
    """

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s %(name)s: %(message)s",
    )

    logging.getLogger("aiogram.event").setLevel(logging.WARNING)

def is_admin(user_id: int) -> bool:
    return user_id in Settings.admins

def gen_random_name(filename: str) -> str:
    """
    генерирует случайное имя файла, сохраняя расширение
    например gen_random_name("test.stl") -> "quOY1U0.stl"
    """

    name, ext = os.path.splitext(filename)
    random_name = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(7))
    return f"{random_name}{ext}"


def validate_fullname(text: str) -> bool:
    """
    валидатор имени и фамилии
    """
    text = text.strip()

    # разбиваем на слова
    parts = text.split()

    if len(parts) < 2:
        return False

    pattern = r"^[A-Za-zА-Яа-яЁё]{2,40}$"

    for part in parts:
        if not re.match(pattern, part):
            return False

    return True


async def send_clean_message(message_or_callback, bot: Bot, state: FSMContext, text: str,
                             reply_markup=None, parse_mode=None):
    data = await state.get_data()

    chat_id = (message_or_callback.message.chat.id
               if isinstance(message_or_callback, CallbackQuery)
               else message_or_callback.chat.id)

    # удалить прошлое сообщение бота
    last_msg = data.get("last_bot_msg")
    if last_msg:
        try:
            await bot.delete_message(chat_id, last_msg)
        except:
            pass

    # отправить новое
    sent = await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )

    await state.update_data(last_bot_msg=sent.message_id)
    return sent